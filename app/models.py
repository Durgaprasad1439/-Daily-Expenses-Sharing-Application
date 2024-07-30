from app import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'mobile_number': self.mobile_number
        }

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    split_method = db.Column(db.String(20), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('created_expenses', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'total_amount': self.total_amount,
            'date': self.date.isoformat(),
            'split_method': self.split_method,
            'created_by_id': self.created_by_id,
            'splits': [split.to_dict() for split in self.splits]
        }

class ExpenseSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('splits', lazy=True))
    expense = db.relationship('Expense', backref=db.backref('splits', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expense_id': self.expense_id,
            'amount': self.amount
        }