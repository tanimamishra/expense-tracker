from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://expense_user:expense_pass@localhost:5432/expense_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    __tablename__ = 'expenses'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    amount      = db.Column(db.Numeric(10, 2), nullable=False)
    category    = db.Column(db.String(60), nullable=False, default='general')
    description = db.Column(db.Text, nullable=True)
    date        = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'amount':      float(self.amount),
            'category':    self.category,
            'description': self.description,
            'date':        self.date.isoformat(),
            'created_at':  self.created_at.isoformat()
        }


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('amount'):
        return jsonify({'error': 'title and amount are required'}), 400
    try:
        expense = Expense(
            title       = data['title'],
            amount      = float(data['amount']),
            category    = data.get('category', 'general'),
            description = data.get('description'),
            date        = datetime.strptime(data['date'], '%Y-%m-%d').date()
                          if data.get('date') else datetime.utcnow().date()
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify(expense.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/expenses', methods=['GET'])
def get_expenses():
    category = request.args.get('category')
    limit    = request.args.get('limit', type=int)
    query = Expense.query.order_by(Expense.date.desc())
    if category:
        query = query.filter_by(category=category)
    if limit:
        query = query.limit(limit)
    expenses = query.all()
    return jsonify({'expenses': [e.to_dict() for e in expenses], 'count': len(expenses)}), 200


@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': f'Expense {expense_id} deleted'}), 200


@app.route('/expenses/summary/<int:year>/<int:month>', methods=['GET'])
def monthly_summary(year, month):
    from sqlalchemy import extract
    expenses = Expense.query.filter(
        extract('year',  Expense.date) == year,
        extract('month', Expense.date) == month
    ).all()
    if not expenses:
        return jsonify({'year': year, 'month': month, 'total': 0, 'count': 0, 'by_category': {}}), 200
    total = sum(float(e.amount) for e in expenses)
    by_category = {}
    for e in expenses:
        by_category[e.category] = round(by_category.get(e.category, 0) + float(e.amount), 2)
    return jsonify({'year': year, 'month': month, 'total': round(total, 2), 'count': len(expenses), 'by_category': by_category}), 200

@app.route('/')
def index():
    return render_template('index.html')

import time

if __name__ == '__main__':
    while True:
        try:
            with app.app_context():
                db.create_all()
            break
        except Exception as e:
            print(f"DB not ready, retrying in 3 seconds... {e}")
            time.sleep(3)
    app.run(host='0.0.0.0', port=5000, debug=True)
