


def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b"Login Admin" in rv.data or b"Login" in rv.data


def test_login_invalid(client):
    rv = client.post('/login', data={'username': 'wrong', 'password': 'wrong'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Invalid credentials" in rv.data


def test_login_valid_redirect(client):
    rv = client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    # Should redirect to /admin/
    assert rv.status_code == 302
    assert '/admin' in rv.headers['Location']


def test_admin_requires_login(client):
    rv = client.get('/admin/')
    # Should redirect to login
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']


def test_admin_dashboard(client):
    # Login first
    client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    rv = client.get('/admin/')
    assert rv.status_code == 200
    assert b"Daftar Smartphone" in rv.data or b"Smartphone List" in rv.data


def test_recommend_select_page(client):
    rv = client.get('/recommend/select')
    assert rv.status_code == 200
    assert b"Cari Rekomendasi Smartphone" in rv.data


def test_recommend_manual_page(client):
    rv = client.get('/recommend/manual')
    assert rv.status_code == 200
    assert b"Manual Input" in rv.data or b"Cari Rekomendasi" in rv.data
