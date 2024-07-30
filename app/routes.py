from datetime import datetime
import os
import io
import csv
from flask import Flask, request, jsonify, send_from_directory, make_response
from app import db
from app.models import User, Expense, ExpenseSplit

def initialize_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Welcome to the Daily Expenses Sharing Application!"})

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(
            email=data['email'],
            name=data['name'],
            mobile_number=data['mobile_number']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201

    @app.route('/expenses', methods=['POST'])
    def add_expense():
        data = request.get_json()

        # Convert date string to a Python date object
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()

        new_expense = Expense(
            description=data['description'],
            total_amount=data['total_amount'],
            date=date_obj,
            split_method=data['split_method'],
            created_by_id=data['created_by_id']
        )
        db.session.add(new_expense)
        db.session.commit()
        
        for split in data['splits']:
            new_split = ExpenseSplit(
                user_id=split['user_id'],
                expense_id=new_expense.id,
                amount=split['amount']
            )
            db.session.add(new_split)
        
        db.session.commit()
        return jsonify({"message": "Expense added successfully!"}), 201

    @app.route('/expenses/<int:user_id>', methods=['GET'])
    def get_user_expenses(user_id):
        expenses = Expense.query.join(ExpenseSplit).filter(ExpenseSplit.user_id == user_id).all()
        return jsonify([expense.to_dict() for expense in expenses]), 200

    @app.route('/expenses/overall', methods=['GET'])
    def get_overall_expenses():
        expenses = Expense.query.all()
        return jsonify([expense.to_dict() for expense in expenses]), 200

    @app.route('/expenses/download', methods=['GET'])
    def download_balance_sheet():
        users = User.query.all()
        balances = {user.id: {"name": user.name, "owed": 0, "owes": 0} for user in users}

        expenses = Expense.query.all()
        for expense in expenses:
            splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()
            for split in splits:
                if split.user_id in balances:
                    balances[split.user_id]["owes"] += split.amount
                else:
                    # If user_id is not in balances, log it for debugging
                    print(f"Warning: User ID {split.user_id} not found in balances")

            if expense.created_by_id in balances:
                balances[expense.created_by_id]["owed"] += expense.total_amount
            else:
                # If created_by_id is not in balances, log it for debugging
                print(f"Warning: Creator User ID {expense.created_by_id} not found in balances")

        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["User", "Owed", "Owes", "Net Balance"])

        for user_id, balance in balances.items():
            net_balance = balance["owed"] - balance["owes"]
            writer.writerow([balance["name"], balance["owed"], balance["owes"], net_balance])

        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=balance_sheet.csv"
        response.headers["Content-type"] = "text/csv"
        return response