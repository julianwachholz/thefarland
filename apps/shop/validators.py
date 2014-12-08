from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from jsonschema import validate as json_validate


ALPHANUMERIC = RegexValidator(
    r'^[\.\w\d-]+$',
    message='Only enter letters and numbers, no spaces.'
)


FIELDS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "minItems": 0,
    "items": {
        "title": "Field",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "display": {
                "type": "string",
            },
            "help_text": {
                "type": "string",
            },
            "field_type": {
                "type": "string",
                "pattern": "^(alpha|email|number)$",
            },
            "min": {
                "description": "Minimum value",
                "type": "number",
            },
            "max": {
                "description": "Maximum value",
                "type": "number",
            },
        },
        "required": ["name", "display", "field_type"],
    },
}


def product_fields_validator(value):
    try:
        json_validate(value, FIELDS_SCHEMA)
    except Exception as e:
        raise ValidationError(e)
