from marshmallow import Schema, fields, validates, ValidationError

class GetOutputsSchema(Schema):
    jobId = fields.String(required=True)