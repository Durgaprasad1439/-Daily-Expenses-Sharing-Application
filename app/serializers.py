from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    mobile_number = fields.Str(required=True, validate=validate.Length(min=10, max=15))

class ExpenseSplitSchema(Schema):
    user_id = fields.Int(required=True)
    amount = fields.Float(allow_none=True)
    percentage = fields.Float(allow_none=True)

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    total_amount = fields.Float(required=True)
    date = fields.Date(required=True)
    split_method = fields.Str(required=True, validate=validate.OneOf(["equal", "exact", "percentage"]))
    created_by_id = fields.Int(required=True)
    splits = fields.List(fields.Nested(ExpenseSplitSchema))

    @validates('splits')
    def validate_splits(self, splits):
        if self.context.get('split_method') == 'percentage':
            total_percentage = sum(split['percentage'] for split in splits)
            if total_percentage != 100:
                raise ValidationError("Percentages must add up to 100%.")