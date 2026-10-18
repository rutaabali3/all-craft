import json
import pytest
import responses
from unittest.mock import patch
from pathlib import Path
from scripts.generate_product_images import generate, API

# Test data setup
MOCK_ROW = {
    "slug": "test-slug",
    "image_path": "projects/test-project/assets/image.png",
    "prompt": "Test prompt"
}

MOCK_IMAGE_URL = "https://example.com/image.png"

@pytest.fixture
def mock_root(tmp_path):
    with patch("scripts.generate_product_images.ROOT", tmp_path):
        yield tmp_path

@responses.activate
def test_generate_success(mock_root):
    # Mock the POST request
    responses.add(
        responses.POST,
        API,
        json={"imageUrl": MOCK_IMAGE_URL},
        status=200
    )

    # Mock the GET request for the image
    mock_image_content = b"x" * 15000  # Size > 10,000 bytes
    responses.add(
        responses.GET,
        MOCK_IMAGE_URL,
        body=mock_image_content,
        status=200
    )

    with patch("scripts.generate_product_images.time.sleep") as mock_sleep:
        result = generate(MOCK_ROW)

    assert result["status"] == "generated"
    assert result["slug"] == MOCK_ROW["slug"]
    assert result["imageUrl"] == MOCK_IMAGE_URL
    assert result["bytes"] == len(mock_image_content)

    # Check that file was written
    expected_path = mock_root / MOCK_ROW["image_path"]
    assert expected_path.exists()
    assert expected_path.read_bytes() == mock_image_content
    assert result["path"] == str(expected_path)

    mock_sleep.assert_not_called()

@responses.activate
def test_generate_network_error(mock_root):
    # Mock the POST request to raise an exception
    responses.add(
        responses.POST,
        API,
        body=Exception("Network error occurred")
    )

    with patch("scripts.generate_product_images.time.sleep") as mock_sleep:
        result = generate(MOCK_ROW)

    assert result["status"] == "failed"
    assert result["slug"] == MOCK_ROW["slug"]
    assert "Exception('Network error occurred')" in result["error"]
    assert mock_sleep.call_count == 3

@responses.activate
def test_generate_invalid_response_missing_image_url(mock_root):
    # Mock the POST request to return valid JSON but missing imageUrl
    responses.add(
        responses.POST,
        API,
        json={"otherField": "someValue"},
        status=200
    )

    with patch("scripts.generate_product_images.time.sleep") as mock_sleep:
        result = generate(MOCK_ROW)

    assert result["status"] == "failed"
    assert result["slug"] == MOCK_ROW["slug"]
    assert "missing imageUrl" in result["error"]
    assert mock_sleep.call_count == 3

@responses.activate
def test_generate_image_too_small(mock_root):
    # Mock the POST request
    responses.add(
        responses.POST,
        API,
        json={"imageUrl": MOCK_IMAGE_URL},
        status=200
    )

    # Mock the GET request to return a small image
    mock_image_content = b"x" * 9999  # Size < 10,000 bytes
    responses.add(
        responses.GET,
        MOCK_IMAGE_URL,
        body=mock_image_content,
        status=200
    )

    with patch("scripts.generate_product_images.time.sleep") as mock_sleep:
        result = generate(MOCK_ROW)

    assert result["status"] == "failed"
    assert result["slug"] == MOCK_ROW["slug"]
    assert "image too small" in result["error"]
    assert mock_sleep.call_count == 3

@responses.activate
def test_generate_retry_success(mock_root):
    # Mock the POST request to fail twice then succeed
    responses.add(
        responses.POST,
        API,
        body=Exception("Network error occurred")
    )
    responses.add(
        responses.POST,
        API,
        body=Exception("Network error occurred")
    )
    responses.add(
        responses.POST,
        API,
        json={"imageUrl": MOCK_IMAGE_URL},
        status=200
    )

    # Mock the GET request to succeed
    mock_image_content = b"x" * 15000  # Size > 10,000 bytes
    responses.add(
        responses.GET,
        MOCK_IMAGE_URL,
        body=mock_image_content,
        status=200
    )

    with patch("scripts.generate_product_images.time.sleep") as mock_sleep:
        result = generate(MOCK_ROW)

    assert result["status"] == "generated"
    assert result["slug"] == MOCK_ROW["slug"]
    assert mock_sleep.call_count == 2

    # Check that sleep was called with expected values (2 * 1, 2 * 2)
    mock_sleep.assert_any_call(2)
    mock_sleep.assert_any_call(4)
