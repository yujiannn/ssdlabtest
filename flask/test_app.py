import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home_page(client):
    """Test the home page."""
    rv = client.get('/')
    assert b'Login' in rv.data

def test_successful_login(client):
    """Test a successful login."""
    rv = client.post('/', data=dict(username='student', password='your_student_id'))
    assert rv.status_code == 302  # Redirection to dashboard
    assert b'session_id' in client.get('/dashboard').data

def test_failed_login(client):
    """Test a failed login."""
    rv = client.post('/', data=dict(username='student', password='wrongpassword'))
    assert b'Invalid username or password' in rv.data

def test_logout(client):
    """Test logout functionality."""
    client.post('/', data=dict(username='student', password='your_student_id'))
    rv = client.get('/logout')
    assert rv.status_code == 302  # Redirect to home
    assert b'Login' in client.get('/').data
