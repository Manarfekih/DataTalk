from datatalk.services import schema_service


def test_get_all_tables():

    tables = schema_service.get_all_tables()

    assert len(tables) > 0

    print(f"\nLoaded {len(tables)} tables.")


def test_validate_tables():

    valid = schema_service.validate_tables(
        [
            "customers",
            "orders",
            "fake_table",
        ]
    )

    assert "customers" in valid
    assert "orders" in valid
    assert "fake_table" not in valid

    print(valid)


def test_get_table_schema():

    schema = schema_service.get_table_schema(
        "customers"
    )

    assert schema is not None
    assert schema.table_name == "customers"

    print(schema)
    