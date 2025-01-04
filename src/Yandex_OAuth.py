from flask import redirect, flash, url_for
from flask_login import login_user

from src import db, yandex
from src.models import User


def handle_oauth_callback(user_info, provider_name, token):
    if not user_info:
        flash(f'Ошибка получения информации о пользователе {provider_name}', 'error')
        return redirect(url_for('login'))

    email = user_info.get('default_email')
    if not email:
        flash(f'Не удалось получить email пользователя от {provider_name}. Пожалуйста попробуйте позже.', 'error')
        return redirect(url_for('login'))

    name = user_info.get('login')
    if not name:
        name = f"user_{user_info.get('id', 'unknown')}"
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        flash(f'Вы успешно вошли через {provider_name}!', 'success')
        user.yandex_access_token = token['access_token']
        db.session.commit()
        return redirect(url_for('main'))
    else:
        new_user = User(
            username=name,
            email=email,
            password='None',
            yandex_access_token=token['access_token']
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Вы успешно авторизовались через {provider_name}!', 'success')
        return redirect(url_for('main'))


def get_user_info(provider, token):
    if provider == 'yandex':
       resp = yandex.get('info', token=token)
       if resp.ok:
            return resp.json()
       else:
            return None
    else:
        return None