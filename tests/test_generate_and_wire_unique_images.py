import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure repository root is in python path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.generate_and_wire_unique_images import generate


@pytest.fixture
def mock_row():
    return {
        "slug": "test-craft",
        "index": "1",
        "image_path": "projects/test-craft/image/item.png",
        "prompt": "a photo of craft item",
    }


@patch("scripts.generate_and_wire_unique_images.time.sleep")
@patch("scripts.generate_and_wire_unique_images.requests.get")
@patch("scripts.generate_and_wire_unique_images.requests.post")
def test_small_image_raises_error_and_fails(mock_post, mock_get, mock_sleep, mock_row, tmp_path):
    post_resp = MagicMock()
    post_resp.json.return_value = {"imageUrl": "https://example.com/small.png"}
    mock_post.return_value = post_resp

    get_resp = MagicMock()
    get_resp.content = b"a" * 9999
    mock_get.return_value = get_resp

    with patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):
        result = generate(mock_row)

    assert result["status"] == "failed"
    assert "image too small: 9999 bytes" in result["error"]
    assert mock_post.call_count == 3
    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 3


@patch("scripts.generate_and_wire_unique_images.time.sleep")
@patch("scripts.generate_and_wire_unique_images.requests.get")
@patch("scripts.generate_and_wire_unique_images.requests.post")
def test_zero_byte_image_fails(mock_post, mock_get, mock_sleep, mock_row, tmp_path):
    post_resp = MagicMock()
    post_resp.json.return_value = {"imageUrl": "https://example.com/empty.png"}
    mock_post.return_value = post_resp

    get_resp = MagicMock()
    get_resp.content = b""
    mock_get.return_value = get_resp

    with patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):
        result = generate(mock_row)

    assert result["status"] == "failed"
    assert "image too small: 0 bytes" in result["error"]


@patch("scripts.generate_and_wire_unique_images.time.sleep")
@patch("scripts.generate_and_wire_unique_images.requests.get")
@patch("scripts.generate_and_wire_unique_images.requests.post")
def test_exact_10000_bytes_succeeds(mock_post, mock_get, mock_sleep, mock_row, tmp_path):
    post_resp = MagicMock()
    post_resp.json.return_value = {"imageUrl": "https://example.com/valid.png"}
    mock_post.return_value = post_resp

    get_resp = MagicMock()
    get_resp.content = b"x" * 10000
    mock_get.return_value = get_resp

    with patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):
        result = generate(mock_row)

    assert result["status"] == "generated"
    assert result["bytes"] == 10000
    assert result["imageUrl"] == "https://example.com/valid.png"
    target = tmp_path / mock_row["image_path"]
    assert target.exists()
    assert len(target.read_bytes()) == 10000


@patch("scripts.generate_and_wire_unique_images.time.sleep")
@patch("scripts.generate_and_wire_unique_images.requests.get")
@patch("scripts.generate_and_wire_unique_images.requests.post")
def test_valid_large_image_succeeds(mock_post, mock_get, mock_sleep, mock_row, tmp_path):
    post_resp = MagicMock()
    post_resp.json.return_value = {"imageUrl": "https://example.com/large.png"}
    mock_post.return_value = post_resp

    get_resp = MagicMock()
    get_resp.content = b"y" * 15000
    mock_get.return_value = get_resp

    with patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):
        result = generate(mock_row)

    assert result["status"] == "generated"
    assert result["bytes"] == 15000
    target = tmp_path / mock_row["image_path"]
    assert target.exists()
    assert len(target.read_bytes()) == 15000


@patch("scripts.generate_and_wire_unique_images.time.sleep")
@patch("scripts.generate_and_wire_unique_images.requests.get")
@patch("scripts.generate_and_wire_unique_images.requests.post")
def test_missing_image_url_fails(mock_post, mock_get, mock_sleep, mock_row, tmp_path):
    post_resp = MagicMock()
    post_resp.json.return_value = {}
    mock_post.return_value = post_resp

    with patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):
        result = generate(mock_row)

    assert result["status"] == "failed"
    assert "missing imageUrl" in result["error"]
