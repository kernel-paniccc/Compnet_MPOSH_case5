from flask import render_template, request, redirect, url_for
from flask_login import login_required

from src.models import Task, admin_required
from src import db, app


@app.route('/buy')
@login_required
@admin_required
def index():
    tasks = Task.query.all()
    return render_template('buy.html', tasks=tasks)


@app.route('/buy/add', methods=['POST'])
@login_required
@admin_required
def add_task():
    task_name = request.form['task_name']
    quantity = request.form['quantity']
    price = request.form['price']
    supplier = request.form['supplier']

    new_task = Task(name=task_name, quantity=quantity, price=price, supplier=supplier)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/buy/delete/<int:task_id>', methods=['POST'])
@login_required
@admin_required
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/buy/edit/<int:task_id>', methods=['POST'])
@login_required
@admin_required
def edit_task(task_id):
    task_to_edit = Task.query.get(task_id)
    if task_to_edit:
        task_to_edit.name = request.form['task_name']
        task_to_edit.quantity = request.form['quantity']
        task_to_edit.price = request.form['price']
        task_to_edit.supplier = request.form['supplier']
        db.session.commit()
    return redirect(url_for('index'))
