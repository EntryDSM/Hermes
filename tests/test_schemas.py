import pytest
from marshmallow import ValidationError

from schema_test_data import AdminSchemaTestData, ApplicantSchemaTestData, ApplicantStatusSchemaTestData


@pytest.mark.parametrize("schema,data,expected_success",
                         AdminSchemaTestData.get_test_data() +
                         ApplicantSchemaTestData.get_test_data() +
                         ApplicantStatusSchemaTestData.get_test_data())
def test_schema(schema, data, expected_success):
    schema = schema()
    try:
        entity = schema.load(data)
        assert schema.dump(entity) == data
    except ValidationError:
        assert not expected_success
