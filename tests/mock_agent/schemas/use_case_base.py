from marshmallow import Schema, fields, validates, ValidationError

class BaseUseCaseSchema(Schema):
    Case = fields.String(required=True)
    Inputs = fields.Dict(keys=fields.String(), values=fields.String(), required=True)
    Outputs = fields.List(fields.String(), required=True)

    @validates('Outputs')
    def no_duplicate_outputs(self, value):
        if len(value) != len(set(value)):
            raise ValidationError('currencies must not contain duplicate elements')