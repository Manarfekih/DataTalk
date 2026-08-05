import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in (
    ROOT / ".venv" / "Lib" / "site-packages",
    ROOT / "src",
):
    if path.exists():
        sys.path.insert(0, str(path))

from datatalk.database.schema import schema_extractor


def test_get_all_tables():
    """The database should contain tables."""

    tables = schema_extractor.get_all_tables()

    assert isinstance(tables, list)
    assert len(tables) > 0

    print(f"\nFound {len(tables)} tables:")
    print(tables)


def test_get_table_schema():
    """A table schema should contain columns."""

    tables = schema_extractor.get_all_tables()

    assert tables

    schema = schema_extractor.get_table_schema(tables[0])

    assert schema is not None
    assert schema.table_name == tables[0]
    assert len(schema.columns) > 0

    print(f"\nTable: {schema.table_name}")

    print("\nColumns:")

    for column in schema.columns:
        print(
            f"  {column.name}"
            f" ({column.data_type})"
        )

    print("\nForeign Keys:")

    for fk in schema.foreign_keys:
        print(
            f"  {fk.constrained_columns}"
            f" -> "
            f"{fk.referred_table}"
        )
