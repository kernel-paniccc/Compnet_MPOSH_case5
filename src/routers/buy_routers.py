from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from src.models import Task, admin_required
from src import db, app
from src.bitrix import create_order_in_bitrix
import logging

@app.route('/buy')
@login_required
@admin_required
def index():
    tasks = Task.query.all()
    logging.info("Загружен список задач")
    return render_template('buy.html', tasks=tasks)


# @app.route('/buy/get_links/<name>/<price>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def get_link(name, price):
#     links = get_products_links(name, price)
#     links = list(set(links))
#     print(links)
#     return render_template('links.html', links=links, name=name)


@app.route('/buy/bitrix/<task_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def bitrix(task_id):
    task = Task.query.get(task_id)
    name = task.name
    quantity = task.quantity
    price = task.price
    supplier = task
    response = create_order_in_bitrix(str(name), int(quantity), int(price), str(supplier))
    if response == 200:
        flash('Заказ успешно создан', category='success')
    else:
        flash('Ошибка при создании заказа', category='error')
    return redirect('/buy')

@app.route('/buy/add', methods=['POST'])
@login_required
@admin_required
def add_task():
    task_name = request.form.get('task_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    supplier = request.form.get('supplier')

    if not task_name or not quantity or not price or not supplier:
        logging.warning("Попытка добавить задачу с незаполненными полями")
        return redirect(url_for('index'))

    new_task = Task(name=task_name, quantity=quantity, price=price, supplier=supplier)
    db.session.add(new_task)
    db.session.commit()
    logging.info(f"Добавлена новая задача: {task_name}")
    return redirect(url_for('index'))


@app.route('/buy/delete/<int:task_id>', methods=['POST'])
@login_required
@admin_required
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        logging.info(f"Задача удалена: {task_to_delete.name}")
    else:
        logging.warning(f"Попытка удалить несуществующую задачу с ID: {task_id}")

    return redirect(url_for('index'))


@app.route('/buy/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_task(task_id):
    task_to_edit = Task.query.get(task_id)

    if request.method == 'POST':
        if task_to_edit:
            task_to_edit.name = request.form.get('task_name')
            task_to_edit.quantity = request.form.get('quantity')
            task_to_edit.price = request.form.get('price')
            task_to_edit.supplier = request.form.get('supplier')

            if not task_to_edit.name or not task_to_edit.quantity or not task_to_edit.price or not task_to_edit.supplier:
                logging.warning("Попытка редактировать задачу с незаполненными полями")
                return redirect(url_for('edit_task', task_id=task_id))

            db.session.commit()
            logging.info(f"Задача отредактирована: {task_to_edit.name}")
        else:
            logging.warning(f"Попытка редактировать несуществующую задачу с ID: {task_id}")
        return redirect(url_for('index'))
