from aiohttp.web import HTTPBadRequest
from marshmallow import Schema, fields, ValidationError
import simplejson as json

DEFAULT_PAGE_SIZE = 20


def validate_page(page_number: int) -> None:
    if page_number < 1:
        raise ValidationError("Must be greater than 1.")


class PaginationSchema(Schema):
    page = fields.Integer(missing=1, validate=validate_page)
    page_size = fields.Integer(missing=DEFAULT_PAGE_SIZE, validate=validate_page)

    def handle_error(self, error, data):
        raise HTTPBadRequest(text=json.dumps(error.messages), content_type='application/json')
