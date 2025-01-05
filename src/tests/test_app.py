import pytest
from src import app, db
from src.models import User, InventoryItem, Applications
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SERVER_NAME'] = 'localhost'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_main_page_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_register(client):
    response = client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_register_password_mismatch(client):
    response = client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='differentpassword'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_register_invalid_email(client):
    response = client.post('/registration', data=dict(
        username='testuser',
        email='invalidemail',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_login(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)

    response = client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_login_invalid_credentials(client):
    response = client.post('/login', data=dict(
        username='nonexistentuser',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_my_inventory(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    response = client.get('/my_inventory')
    assert response.status_code == 200

def test_admin_panel(client):
    admin_user = User(username='admin', email='admin@example.com', password=str(generate_password_hash('admin')), role='admin')
    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()

    client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)

    response = client.get('/admin')
    assert response.status_code == 200

def test_add_inventory_item(client):
    admin_user = User(username='admin', email='admin@example.com', password=str(generate_password_hash('admin')), role='admin')
    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()
    client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)

    response = client.post('/admin/inventory_add', data=dict(
        name='Test Item',
        quantity=10,
        status='available'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_get_user_applet(client):
    admin_user = User(username='admin', email='admin@example.com', password=str(generate_password_hash('admin')), role='admin')
    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()
    client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)

    response = client.get('/admin/get_user_applet')
    assert response.status_code == 200

def test_logout(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_apply_for_inventory(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    with app.app_context():
        item = InventoryItem(name='Test Item', quantity=10, status='available')
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)

    response = client.post('/applications', data=dict(
        item_id=item.id,
        value='5'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_return_inventory(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    with app.app_context():
        item = InventoryItem(name='Test Item', quantity=10, status='available')
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)

        application = Applications(user_id=1, count=5, name='Test Item', status='accepted', item_id=item.id, item_name='Test Item')
        db.session.add(application)
        db.session.commit()
        db.session.refresh(application)

    response = client.post(f'/return_item/{application.id}', follow_redirects=True)
    assert response.status_code == 200


def test_view_user_applications(client):
    client.post('/registration', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        password_return='password'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    with app.app_context():
        application = Applications(user_id=1, count=5, name='Test Item', status='not accepted', item_id=1, item_name='Test Item')
        db.session.add(application)
        db.session.commit()

    response = client.get('/account')
    assert response.status_code == 200