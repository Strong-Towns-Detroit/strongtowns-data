import pyarrow as pa
import pyarrow.parquet as pq

from krabby_real_estate.data.hashing import schema_hash


def test_schema_hash_survives_parquet_list_child_name_normalization(tmp_path):
    schema = pa.schema(
        [
            pa.field(
                "values",
                pa.list_(pa.struct([pa.field("key", pa.string()), pa.field("value", pa.string())])),
                nullable=False,
            )
        ]
    )
    table = pa.Table.from_pydict({"values": [[{"key": "a", "value": "b"}]]}, schema=schema)
    path = tmp_path / "records.parquet"
    pq.write_table(table, path)
    restored = pq.ParquetFile(path).schema_arrow
    assert restored.equals(schema, check_metadata=False)
    assert schema_hash(restored) == schema_hash(schema)
