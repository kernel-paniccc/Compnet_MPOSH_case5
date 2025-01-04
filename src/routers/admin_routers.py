from flask import render_template, request, redirect, flash
from flask_login import login_required
from src.models import Aplications, InventoryItem, admin_required, log_to_db, ReturnAplication
from src import app, db

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_panel():
    Reports = ReturnAplication.query.all()
    clear_reports = []
    for report in Reports:
        if len([el for el in Aplications.query.filter_by(id=report.item_id).all()]) > 0:
            clear_reports.append(report)
        else:
            db.session.delete(report)
            db.session.commit()
    Reports = clear_reports
    return render_template('admin.html', reports=Reports)


@app.route('/admin/del_report/<int:report_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def del_report(report_id):
    report = ReturnAplication.query.get(report_id)
    db.session.delete(report)
    db.session.commit()
    return redirect('/admin')


@app.route('/admin/get_user_applet', methods=['GET', 'POST'])
@login_required
@admin_required
def get_user_applet():
    applet = Aplications.query.all()
    return render_template('get_user_applet.html', applets=applet)


@app.route('/admin/inventory_add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_inventory_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        status = request.form['status']
        item = InventoryItem.query.filter_by(name=name, status=status).first()
        if item:
            item.quantity += int(quantity)
            db.session.commit()
            log_to_db(f"Добавлен инвентарный элемент: {name}, количество: {quantity}, статус: {status}")
            flash("Инвентарь добавлен", category='success')
        else:
            new_item = InventoryItem(name=name, quantity=quantity, status=status)
            db.session.add(new_item)
            db.session.commit()
            log_to_db(f"Добавлен инвентарный элемент: {name}, количество: {quantity}, статус: {status}")
            flash("Инвентарь добавлен", category='success')
    return render_template('add_inventory_item.html')


@app.route('/admin/all_item', methods=['GET', 'POST'])
@login_required
@admin_required
def all_inventory_item():
    items = InventoryItem.query.all()
    return render_template('all_items.html', items=items)


@app.route('/admin/del_applet/<int:applet_id>')
@login_required
@admin_required
def delited_applet(applet_id):
    item = Aplications.query.get(applet_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        log_to_db(f"Запись приложения удалена: ID {applet_id}")
        flash('Запись удалена', 'success')
    else:
        log_to_db(f"Попытка удалить запись приложения не удалась: ID {applet_id} не найден")
        flash('Запись не найдена', 'error')
    return redirect('/admin/get_user_applet')


@app.route('/admin/edit_applet_status/<int:applet_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_applet(applet_id):
    applet = Aplications.query.get(applet_id)
    if not applet:
        log_to_db(f"Попытка редактирования статуса приложения не удалась: ID {applet_id} не найден")
        flash('Приложение не найдено', 'error')
        return redirect('/admin/all_applet')
    if request.method == 'POST':
        new_status = request.form['status']
        if applet.status != new_status:
            item = InventoryItem.query.get(applet.item_id)
            if new_status == 'not accepted' and applet.status !='return':
                if item:
                    item.quantity += applet.count
                    log_to_db(f"Количество для {item.name} увеличено на {applet.count}")
                    flash(f'Количество для {item.name} увеличено на {applet.count}', 'success')
                applet.status = new_status
            elif new_status == 'accepted':
                if item:
                    if item.quantity >= applet.count:
                        item.quantity -= applet.count
                        log_to_db(f"Количество для {item.name} уменьшено на {applet.count}")
                        flash(f'Количество для {item.name} уменьшено на {applet.count}', 'success')
                        applet.status = new_status
                    else:
                        flash(f'Недостаточно количества для {item.name}', 'error')
                        log_to_db(
                            f"Не удалось изменить статус приложения ID {applet_id}: недостаточно количества для {item.name}")
                        return redirect('/admin/get_user_applet')
                else:
                    flash('Товар не найден в инвентаре', 'error')
                    log_to_db(f"Не удалось изменить статус приложения ID {applet_id}: товар не найден")
            else:
                applet.status = new_status
                flash('Заявка возврата изменила статус на "не принято"', category='success')
                log_to_db(f"Заявка возврата изменила статус на 'не принято'")
            db.session.commit()
            log_to_db(f"Статус приложения изменен: ID {applet_id}, новый статус: {new_status}")
    return redirect('/admin/get_user_applet')


@app.route('/admin/del/<int:item_id>')
@login_required
@admin_required
def delited(item_id):
    item = InventoryItem.query.get(item_id)
    applets = Aplications.query.filter_by(item_id=item_id).all()
    if item:
        for applet in applets:
            db.session.delete(applet)
        db.session.delete(item)
        db.session.commit()
        log_to_db(f"Запись инвентарного элемента удалена: ID {item_id}")
        flash('Запись удалена', 'success')
    else:
        log_to_db(f"Попытка удалить инвентарный элемент не удалась: ID {item_id} не найден")
        flash('Запись не найдена', 'error')
    return redirect('/admin/all_item')

@app.route('/admin/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    item = InventoryItem.query.get(item_id)
    if not item:
        log_to_db(f"Попытка редактирования инвентарного элемента не удалась: ID {item_id} не найден")
        return redirect('/admin')

    if request.method == 'POST':
        old_name = item.name
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.status = request.form['status']
        db.session.commit()
        log_to_db(
            f"Данные инвентарного элемента изменены: ID {item_id}, старое имя: {old_name}, новое имя: {item.name}")

    return redirect('/admin/all_item')


@app.route('/admin/get_logs')
@login_required
@admin_required
def get_logs():
    return redirect('/log')

