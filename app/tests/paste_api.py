from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_create_paste_api_success():
    with patch('app.services.paste_service.generate_shortlink', return_value='testlink'), \
         patch('app.services.paste_service.save_paste_to_storage') as mock_save, \
         patch('app.db.repository.create_paste') as mock_create:
        response = client.post("/paste/", json={"paste_contents": "Hello, world!", "expires_at": 60})
        assert response.status_code == 200
        assert response.json() == {"shortlink": "testlink"}
        mock_save.assert_called_once_with('testlink', 'Hello, world!')
        mock_create.assert_called_once()

def test_retrieve_paste_api_not_found():
    with patch('app.services.paste_service.get_paste_service', return_value=None), \
         patch('app.services.paste_service.get_paste_content_from_storage', return_value=None):
        response = client.get("/paste/?shortlink=testlink")
        assert response.status_code == 404
        assert response.json() == {"detail": "Paste not found"}

def test_delete_paste_api_success():
    with patch('app.services.paste_service.get_paste_service', return_value=True), \
         patch('app.services.paste_service.delete_paste_service', return_value=True) as mock_delete:
        response = client.delete("/paste/?shortlink=testlink")
        assert response.status_code == 200
        assert response.json() == {"message": "Paste deleted successfully"}
        mock_delete.assert_called_once_with(any(Session), 'testlink')

def test_delete_paste_api_not_found():
    with patch('app.services.paste_service.get_paste_service', return_value=None):
        response = client.delete("/paste/?shortlink=testlink")
        assert response.status_code == 404
        assert response.json() == {"detail": "Paste not found"}

def test_create_paste_empty_expires_at():
    with patch('app.services.paste_service.generate_shortlink', return_value='testlink'), \
         patch('app.services.paste_service.save_paste_to_storage') as mock_save, \
         patch('app.db.repository.create_paste') as mock_create:
        response = client.post("/paste/", json={"paste_contents": "Hello, world!", "expires_at": ""})
        assert response.status_code == 200
        assert response.json() == {"shortlink": "testlink"}
        mock_save.assert_called_once_with('testlink', 'Hello, world!')
        mock_create.assert_called_once()

def test_create_paste_invalid_contents():
    with patch('app.services.paste_service.generate_shortlink', return_value='testlink'), \
         patch('app.services.paste_service.save_paste_to_storage') as mock_save, \
         patch('app.db.repository.create_paste') as mock_create:
        response = client.post("/paste/", json={"paste_contents": "", "expires_at": 60})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid paste contents"}
        mock_save.assert_not_called()
        mock_create.assert_not_called()