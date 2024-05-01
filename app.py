from flask import Flask, render_template, url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer,nullable=False)
    date  = db.Column(db.DateTime,default=datetime.now())
    category = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.id 

@app.route('/',methods=['POST','GET'])
def index(): 
    if request.method == 'POST':
        amount_spent = request.form['amount']
        category_spent = request.form['category']
        description_spent = request.form['description']
        new_expense = Expense(amount=amount_spent,category=category_spent,description=description_spent)
        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your expense!"
    else:
        category_filter = request.args.get('category')
        if category_filter:
            expenses = Expense.query.filter_by(category=category_filter).order_by(Expense.date).all()
        else:
            expenses = Expense.query.order_by(Expense.date).all()
        total_expenses = sum( expense.amount for expense in expenses )
        budget = 20000
        remaining_balance = budget - total_expenses
        return render_template('index.html',expenses=expenses,total_expenses=total_expenses,remaining_balance=remaining_balance)



@app.route('/delete/<int:id>')
def delete(id):
    del_expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(del_expense)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting expense"
    

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    expense = Expense.query.get_or_404(id)
    if request.method == "POST":
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        expense.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "An issue occured while updating task!"
    else:
        return render_template('update.html',expense=expense)
    
with app.app_context():
    db.create_all()
if __name__ == "main":
    app.run(debug=True)