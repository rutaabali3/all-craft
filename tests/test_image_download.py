from unittest.mock import MagicMock, patch
import pytest
import sys
from pathlib import Path

# Add repo root and scripts directory to sys.path if needed
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import generate_and_wire_unique_images, generate_product_images


def test_generate_unique_images_streaming(tmp_path):
    target_path = tmp_path / "test_img.png"
    row = {
        "slug": "test-slug",
        "index": "1",
        "prompt": "test prompt",
        "image_path": str(target_path.relative_to(ROOT) if target_path.is_relative_to(ROOT) else target_path),
    }

    mock_post_resp = MagicMock()
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/test.png"}
    mock_post_resp.raise_for_status.return_value = None

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.iter_content.return_value = [b"a" * 5000, b"b" * 6000]
    mock_get_resp.__enter__.return_value = mock_get_resp

    with patch("scripts.generate_and_wire_unique_images.requests.post", return_value=mock_post_resp), \
         patch("scripts.generate_and_wire_unique_images.requests.get", return_value=mock_get_resp), \
         patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path):

        # Adjust row path relative to tmp_path
        row["image_path"] = "test_img.png"
        result = generate_and_wire_unique_images.generate(row)

        assert result["status"] == "generated"
        assert result["bytes"] == 11000
        actual_target = tmp_path / "test_img.png"
        assert actual_target.exists()
        assert len(actual_target.read_bytes()) == 11000


def test_generate_unique_images_too_small(tmp_path):
    mock_post_resp = MagicMock()
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/test.png"}
    mock_post_resp.raise_for_status.return_value = None

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.iter_content.return_value = [b"a" * 1000]
    mock_get_resp.__enter__.return_value = mock_get_resp

    with patch("scripts.generate_and_wire_unique_images.requests.post", return_value=mock_post_resp), \
         patch("scripts.generate_and_wire_unique_images.requests.get", return_value=mock_get_resp), \
         patch("scripts.generate_and_wire_unique_images.ROOT", tmp_path), \
         patch("scripts.generate_and_wire_unique_images.time.sleep"):

        row = {"slug": "test-slug", "index": "1", "prompt": "test prompt", "image_path": "small_img.png"}
        result = generate_and_wire_unique_images.generate(row)

        assert result["status"] == "failed"
        assert "image too small" in result["error"]
        actual_target = tmp_path / "small_img.png"
        assert not actual_target.exists()


def test_generate_product_images_streaming(tmp_path):
    mock_post_resp = MagicMock()
    mock_post_resp.json.return_value = {"imageUrl": "http://example.com/test.png"}
    mock_post_resp.raise_for_status.return_value = None

    mock_get_resp = MagicMock()
    mock_get_resp.raise_for_status.return_value = None
    mock_get_resp.iter_content.return_value = [b"x" * 6000, b"y" * 5000]
    mock_get_resp.__enter__.return_value = mock_get_resp

    with patch.object(generate_product_images.session, "post", return_value=mock_post_resp), \
         patch.object(generate_product_images.session, "get", return_value=mock_get_resp), \
         patch("scripts.generate_product_images.ROOT", tmp_path):

        row = {"slug": "prod-slug", "prompt": "test prompt", "image_path": "prod_img.png"}
        result = generate_product_images.generate(row)

        assert result["status"] == "generated"
        assert result["bytes"] == 11000
        actual_target = tmp_path / "prod_img.png"
        assert actual_target.exists()
        assert len(actual_target.read_bytes()) == 11000
