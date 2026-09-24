from unittest.mock import MagicMock, patch
import pytest
import requests
from scripts.generate_product_images import generate


@pytest.fixture
def sample_row(tmp_path):
    target_path = tmp_path / "images" / "test_item.png"
    return {
        "slug": "test-item",
        "prompt": "A cool test product image",
        "image_path": str(target_path),
    }


def test_generate_success_first_attempt(sample_row, monkeypatch):
    mock_post_resp = MagicMock()
    mock_post_resp.raise_for_status.return_value = None
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/image.png"}

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.content = b"x" * 10500

    mock_session = MagicMock()
    mock_session.post.return_value = mock_post_resp
    mock_session.get.return_value = mock_get_resp

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "generated"
    assert result["slug"] == "test-item"
    assert result["bytes"] == 10500
    assert result["imageUrl"] == "http://example.com/image.png"

    mock_post_resp.raise_for_status.assert_called_once()
    mock_get_resp.raise_for_status.assert_called_once()
    mock_sleep.assert_not_called()


def test_generate_retry_and_succeed(sample_row):
    mock_post_fail = MagicMock()
    mock_post_fail.raise_for_status.side_effect = requests.RequestException("Transient error")

    mock_post_success = MagicMock()
    mock_post_success.raise_for_status.return_value = None
    mock_post_success.json.return_value = {"imageUrl": "http://example.com/image.png"}

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.content = b"y" * 12000

    mock_session = MagicMock()
    mock_session.post.side_effect = [mock_post_fail, mock_post_success]
    mock_session.get.return_value = mock_get_resp

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "generated"
    assert mock_session.post.call_count == 2
    mock_sleep.assert_called_once_with(2)  # 2 * attempt 1


def test_generate_max_retries_failed(sample_row):
    mock_session = MagicMock()
    mock_session.post.side_effect = requests.RequestException("Persistent outage")

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "failed"
    assert "Persistent outage" in result["error"]
    assert mock_session.post.call_count == 3
    assert mock_sleep.call_args_list == [
        ((2,),),
        ((4,),),
        ((6,),),
    ]


def test_generate_missing_image_url(sample_row):
    mock_post_resp = MagicMock()
    mock_post_resp.raise_for_status.return_value = None
    mock_post_resp.json.return_value = {}  # No imageUrl

    mock_session = MagicMock()
    mock_session.post.return_value = mock_post_resp

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "failed"
    assert "missing imageUrl" in result["error"]
    assert mock_session.post.call_count == 3


def test_generate_image_too_small(sample_row):
    mock_post_resp = MagicMock()
    mock_post_resp.raise_for_status.return_value = None
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/small.png"}

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.content = b"tiny"  # < 10000 bytes

    mock_session = MagicMock()
    mock_session.post.return_value = mock_post_resp
    mock_session.get.return_value = mock_get_resp

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "failed"
    assert "image too small" in result["error"]
    assert mock_session.get.call_count == 3


def test_generate_download_http_error(sample_row):
    mock_post_resp = MagicMock()
    mock_post_resp.raise_for_status.return_value = None
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/404.png"}

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    mock_session = MagicMock()
    mock_session.post.return_value = mock_post_resp
    mock_session.get.return_value = mock_get_resp

    mock_sleep = MagicMock()

    with patch("scripts.generate_product_images.session", mock_session), \
         patch("time.sleep", mock_sleep):
        result = generate(sample_row)

    assert result["status"] == "failed"
    assert "404 Not Found" in result["error"]
    assert mock_session.get.call_count == 3
