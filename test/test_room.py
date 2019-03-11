from app.main import MainSetup

APP = MainSetup.get_app()


def test_room_create():
    data = {
        'name': 'Room1',
    }
    request, response = APP.test_client.post('/room', data)
    assert response.status == 200


def test_change_room_name():
    request, response = APP.test_client.put('/')
    assert response.status == 405


def test_add_user_to_room():
    request, response = APP.test_client.put('/')
    assert response.status == 405


def test_remove_user_from_room():
    request, response = APP.test_client.put('/')
    assert response.status == 405
