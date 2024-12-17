from flask import request, render_template, redirect, flash
from flask_login import login_required
from src import app, db
from src.models import InventoryItem, Aplications, admin_required


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')

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
        new_item = InventoryItem(name=name, quantity=quantity, status=status)
        db.session.add(new_item)
        db.session.commit()
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
        flash('Запись удалена', 'success')
    else:
        flash('Запись не найдена', 'error')
    return redirect('/admin/get_user_applet')


@app.route('/admin/edit_applet_status/<int:applet_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_applet(applet_id):
    applet = Aplications.query.get(applet_id)
    if not applet:
        return redirect('/admin/all_applet')
    if request.method == 'POST':
        new_status = request.form['status']
        if applet.status != new_status:
            if new_status == 'not accepted':
                item = InventoryItem.query.get(applet.item_id)
                if item:
                    item.quantity += applet.count
                    flash(f'Количество для {item.name} увеличено на {applet.count}', 'success')
            if new_status == 'accepted':
                item = InventoryItem.query.get(applet.item_id)
                if item:
                    if item.quantity >= applet.count:
                        item.quantity -= applet.count
                        flash(f'Количество для {item.name} уменьшено на {applet.count}', 'success')
                    else:
                        flash(f'Недостаточно количества для {item.name}', 'error')
                        applet.status = 'not accepted'
            applet.status = new_status
            db.session.commit()
            return redirect('/admin/get_user_applet')
    return render_template('edit_applet.html', app=applet)


# @app.route('/admin/refreash_database', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def refreash_database():
#     applets = Aplications.query.all()
#     for applet in applets:
#         if applet.status == 'accepted':
#             item = InventoryItem.query.get(applet.item_id)
#             if item:
#                 if item.quantity >= applet.count:
#                     item.quantity -= applet.count
#                     flash(f'Количество для {item.name} уменьшено на {applet.count}', 'success')
#                 else:
#                     flash(f'Недостаточно количества для {item.name}', 'error')
#                     applet.status = 'not accepted'
#             else:
#                 flash(f'Товар с ID {applet.item_id} не найден', 'error')
#     db.session.commit()
#     return redirect('/admin/get_user_applet')


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
        flash('Запись удалена', 'success')
    else:
        flash('Запись не найдена', 'error')
    return redirect('/admin/all_item')

@app.route('/admin/edit/<int:item_edit_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_edit_id):
    item = InventoryItem.query.get(item_edit_id)
    if not item: return redirect('/admin')
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.status = request.form['status']
        db.session.commit()
        flash('Данные изменены', 'success')
        return redirect('/admin/all_item')
    return render_template('edit_item.html', item=item)