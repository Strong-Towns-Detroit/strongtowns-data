from pathlib import Path


def test_data_package_does_not_import_graphics_or_consumers():
    source_root = Path(__file__).parents[1] / "src" / "strongtowns_data"
    source = "\n".join(path.read_text() for path in source_root.rglob("*.py"))

    assert "strongtowns_graphics" not in source
    assert "krabby_real_estate" not in source
    assert "strongtowns_detroit" not in source
