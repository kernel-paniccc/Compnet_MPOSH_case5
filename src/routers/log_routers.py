from flask_login import login_required

from src import app
from src.models import Log, admin_required
from flask import render_template, request, send_file, flash, redirect, url_for
from io import BytesIO
import pandas as pd
from datetime import datetime

@app.route('/log', methods=['GET', 'POST'])
@login_required
@admin_required
def view_logs():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            logs = Log.query.filter(Log.created_at >= start_date, Log.created_at <= end_date).all()
        except ValueError:
            logs = Log.query.all()  # В случае ошибки, показываем все логи
            flash('Неверный формат даты. Пожалуйста, используйте YYYY-MM-DD.', 'error')
    else:
        logs = Log.query.all()

    return render_template('logs_main.html', logs=logs)

@app.route('/log/download_logs', methods=['POST'])
@login_required
@admin_required
def download_logs():
    log_ids = request.form.getlist('log_ids')
    if not log_ids:
        flash('Выберите хотя бы один лог для скачивания', 'error')
        return redirect(url_for('view_logs'))

    logs = Log.query.filter(Log.id.in_(log_ids)).all()
    df = pd.DataFrame([(log.id, log.description, log.created_at) for log in logs],
                      columns=['ID', 'Description', 'Created At'])
    output = BytesIO()
    df.to_csv(output, index=False, encoding='windows-1251')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='selected_logs.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
