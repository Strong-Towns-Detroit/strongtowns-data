"""Normalize BZA minutes filenames."""

import datetime
import os
import re


def parse_date(filename):
    """Extract a date from a BZA minutes PDF filename.

    Tries multiple patterns (month words, numeric, 8-digit, 7-digit).
    Returns a datetime.date or None.
    """
    name = os.path.splitext(filename)[0]
    name_lower = name.lower()
    iso = re.search(r"(?<!\d)(\d{4})[-_](\d{2})[-_](\d{2})(?!\d)", name)
    if iso:
        return convert_to_date(iso.group(2), iso.group(3), iso.group(1))

    months = (
        r"(january|february|march|april|may|june|july|august|september|"
        r"october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)"
    )

    match = re.search(rf"{months}[^0-9]+([0-9]{{1,2}})[^0-9]+([0-9]{{4}})", name_lower)
    if match:
        return convert_to_date(match.group(1), match.group(2), match.group(3))

    match = re.search(r"([0-9]{1,2})[-_]([0-9]{1,2})[-_]([0-9]{4})", name_lower)
    if match:
        return convert_to_date(match.group(1), match.group(2), match.group(3))

    match = re.search(r"(?<!\d)([0-9]{8})(?!\d)", name_lower)
    if match:
        s = match.group(1)
        return convert_to_date(s[:2], s[2:4], s[4:])

    match = re.search(r"(?<!\d)([0-9]{7})(?!\d)", name_lower)
    if match:
        s = match.group(1)
        return convert_to_date(s[:1], s[1:3], s[3:]) or convert_to_date(
            s[:2], s[2:3], s[3:]
        )

    return None


def convert_to_date(m, d, y):
    """Convert month/day/year strings to a datetime.date.

    Month can be numeric or a name/abbreviation. Returns None on invalid input.
    """
    month_map = {
        "january": 1,
        "jan": 1,
        "february": 2,
        "feb": 2,
        "feb.": 2,
        "march": 3,
        "mar": 3,
        "april": 4,
        "apr": 4,
        "may": 5,
        "june": 6,
        "jun": 6,
        "july": 7,
        "jul": 7,
        "august": 8,
        "aug": 8,
        "september": 9,
        "sep": 9,
        "sept": 9,
        "sept.": 9,
        "october": 10,
        "oct": 10,
        "oct.": 10,
        "november": 11,
        "nov": 11,
        "nov.": 11,
        "december": 12,
        "dec": 12,
    }

    try:
        if m.lower() in month_map:
            month = month_map[m.lower()]
        else:
            month = int(m)

        day = int(d)
        year = int(y)

        return datetime.date(year, month, day)
    except ValueError:
        return None
