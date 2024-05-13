import pytest
from unittest.mock import patch, MagicMock
from app.main import generate_shortlink, save_paste_to_storage, delete_paste_service

class TestPasteService:
    def test_generate_shortlink_happy_path(self):
        shortlink = generate_shortlink()
        assert len(shortlink) == 5
        assert isinstance(shortlink, str)
        assert all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in shortlink)

    @patch('app.main.save_to_s3')
    def test_save_paste_to_storage_error_handling(self, mock_save_to_s3):
        mock_save_to_s3.side_effect = Exception("S3 failure")
        with pytest.raises(Exception) as excinfo:
            save_paste_to_storage("testlink", "content")
        assert "Failed to save paste to storage: S3 failure" in str(excinfo.value)

    @patch('app.main.delete_paste')
    @patch('app.main.delete_from_s3')
    def test_delete_paste_service_success(self, mock_delete_from_s3, mock_delete_paste):
        mock_delete_paste.return_value = True
        mock_delete_from_s3.return_value = None
        result = delete_paste_service(MagicMock(), "testlink")
        assert result == True
        mock_delete_paste.assert_called_once_with(MagicMock(), "testlink")
        mock_delete_from_s3.assert_called_once_with("testlink")

    @patch('app.main.save_to_s3')
    def test_save_paste_to_storage_success(self, mock_save_to_s3):
        mock_save_to_s3.return_value = None
        result = save_paste_to_storage("testlink", "content")
        assert result == None
        mock_save_to_s3.assert_called_once_with("testlink", "content")

    def test_generate_shortlink_success(self):
        shortlink = generate_shortlink()
        assert len(shortlink) == 5
        assert isinstance(shortlink, str)
        assert all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in shortlink)

    @patch('app.main.save_to_s3')
    def test_save_empty_paste_to_storage_success(self, mock_save_to_s3):
        mock_save_to_s3.return_value = None
        result = save_paste_to_storage("testlink", "")
        assert result == None
        mock_save_to_s3.assert_called_once_with("testlink", "")

    @patch('app.main.delete_paste')
    @patch('app.main.delete_from_s3')
    def test_delete_nonexistent_paste_service(self, mock_delete_from_s3, mock_delete_paste):
        mock_delete_paste.return_value = False
        result = delete_paste_service(MagicMock(), "nonexistentlink")
        assert result == False
        mock_delete_paste.assert_called_once_with(MagicMock(), "nonexistentlink")
        mock_delete_from_s3.assert_not_called()

    @patch('app.main.save_to_s3')
    def test_save_empty_paste_to_storage_success(self, mock_save_to_s3):
        mock_save_to_s3.return_value = None
        result = save_paste_to_storage("testlink", "")
        assert result == None
        mock_save_to_s3.assert_called_once_with("testlink", "")

    @patch('app.main.delete_paste')
    @patch('app.main.delete_from_s3')
    def test_delete_nonexistent_paste_service(self, mock_delete_from_s3, mock_delete_paste):
        mock_delete_paste.return_value = False
        result = delete_paste_service(MagicMock(), "nonexistentlink")
        assert result == False
        mock_delete_paste.assert_called_once_with(MagicMock(), "nonexistentlink")
        mock_delete_from_s3.assert_not_called()

    @patch('app.main.save_to_s3')
    def test_save_paste_with_long_content_to_storage_success(self, mock_save_to_s3):
        long_content = "a" * 1000
        mock_save_to_s3.return_value = None
        result = save_paste_to_storage("testlink", long_content)
        assert result == None
        mock_save_to_s3.assert_called_once_with("testlink", long_content)

    @patch('app.main.delete_paste')
    @patch('app.main.delete_from_s3')
    def test_delete_paste_from_storage_network_error_handling(self, mock_delete_from_s3, mock_delete_paste):
        mock_delete_paste.side_effect = requests.exceptions.RequestException("Network error")
        result = delete_paste_service(MagicMock(), "testlink")
        assert result == False
        mock_delete_paste.assert_called_once_with(MagicMock(), "testlink")
        mock_delete_from_s3.assert_not_called()