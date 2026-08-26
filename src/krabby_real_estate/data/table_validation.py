"""Strict Arrow table validation without implicit type coercion."""

from __future__ import annotations

from collections.abc import Iterable

import pyarrow as pa
import pyarrow.compute as pc

from krabby_real_estate.data.hashing import schema_hash
from krabby_real_estate.data.model import DatasetContract, ValidationIssue, ValidationResult


def validate_table(table: pa.Table, contract: DatasetContract) -> ValidationResult:
    result = ValidationResult()
    if contract.arrow_schema is not None:
        result.require(
            table.schema.equals(contract.arrow_schema, check_metadata=False),
            "schema_mismatch",
            f"expected schema {schema_hash(contract.arrow_schema)}, got {schema_hash(table.schema)}",
        )
        for field in contract.arrow_schema:
            if not field.nullable and field.name in table.column_names:
                null_count = table[field.name].null_count
                result.require(
                    null_count == 0,
                    "null_not_allowed",
                    f"{field.name} contains {null_count} nulls",
                )
    for key in contract.primary_key:
        if key not in table.column_names:
            result.issues.append(ValidationIssue("missing_primary_key", key))
            continue
        column = table[key]
        if column.null_count:
            result.issues.append(
                ValidationIssue("null_primary_key", f"{key} contains {column.null_count} nulls")
            )
    if contract.primary_key and all(key in table.column_names for key in contract.primary_key):
        columns = [table[key].combine_chunks().to_pylist() for key in contract.primary_key]
        if len(set(zip(*columns, strict=True))) != len(table):
            result.issues.append(ValidationIssue("duplicate_primary_key", "primary key not unique"))
    for validator in contract.validators:
        result.extend(validator(table))
    return result


def enum_validator(column: str, allowed: Iterable[str]):
    allowed_values = frozenset(allowed)

    def validate(table: pa.Table) -> ValidationResult:
        result = ValidationResult()
        if column not in table.column_names:
            return result
        actual = set(pc.unique(table[column]).to_pylist()) - {None}
        invalid = sorted(actual - allowed_values)
        result.require(
            not invalid,
            "invalid_enum",
            f"{column} contains values outside {sorted(allowed_values)}: {invalid}",
        )
        return result

    return validate


def range_validator(column: str, minimum: float, maximum: float):
    def validate(table: pa.Table) -> ValidationResult:
        result = ValidationResult()
        if column not in table.column_names or len(table) == 0:
            return result
        values = table[column]
        below = pc.any(pc.less(values, pa.scalar(minimum))).as_py()
        above = pc.any(pc.greater(values, pa.scalar(maximum))).as_py()
        result.require(
            not below and not above,
            "out_of_range",
            f"{column} must be within [{minimum}, {maximum}]",
        )
        return result

    return validate


def conditional_required_validator(
    condition_column: str, condition_values: Iterable[str], required_columns: Iterable[str]
):
    conditions = frozenset(condition_values)
    required = tuple(required_columns)

    def validate(table: pa.Table) -> ValidationResult:
        result = ValidationResult()
        if condition_column not in table.column_names:
            return result
        missing_columns = [name for name in required if name not in table.column_names]
        if missing_columns:
            result.issues.append(
                ValidationIssue(
                    "conditional_required_definition",
                    f"missing columns: {missing_columns}",
                )
            )
            return result
        condition_list = table[condition_column].combine_chunks().to_pylist()
        for column in required:
            values = table[column].combine_chunks().to_pylist()
            missing_count = sum(
                condition in conditions and (value is None or value == "")
                for condition, value in zip(condition_list, values, strict=True)
            )
            result.require(
                missing_count == 0,
                "conditional_value_missing",
                f"{column} is missing for {missing_count} final review decisions",
            )
        return result

    return validate


def validate_foreign_key(
    child: pa.Table,
    child_columns: tuple[str, ...],
    parent: pa.Table,
    parent_columns: tuple[str, ...],
) -> ValidationResult:
    result = ValidationResult()
    if len(child_columns) != len(parent_columns):
        result.issues.append(ValidationIssue("foreign_key_definition", "foreign-key arity differs"))
        return result
    missing = [name for name in child_columns if name not in child.column_names]
    missing += [name for name in parent_columns if name not in parent.column_names]
    if missing:
        result.issues.append(
            ValidationIssue("foreign_key_definition", f"missing columns: {sorted(missing)}")
        )
        return result
    child_values = set(
        zip(
            *(child[name].combine_chunks().to_pylist() for name in child_columns),
            strict=True,
        )
    )
    parent_values = set(
        zip(
            *(parent[name].combine_chunks().to_pylist() for name in parent_columns),
            strict=True,
        )
    )
    orphans = child_values - parent_values
    result.require(
        not orphans,
        "foreign_key_violation",
        f"{len(orphans)} child keys have no parent",
    )
    return result
