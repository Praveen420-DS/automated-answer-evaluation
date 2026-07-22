from __future__ import annotations

import uuid
from pathlib import Path

import cv2


def validate_image(path: str | Path) -> Path:
    image_path = Path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Invalid or unreadable image: {image_path}")

    return image_path


def preprocess_image(
    path: str | Path,
    enabled: bool = False,
    output_dir: str | Path | None = None,
) -> Path:
    """Return the original image or a processed PNG in the supplied workspace."""
    image_path = validate_image(path)
    if not enabled:
        return image_path

    if output_dir is None:
        raise ValueError("output_dir is required when preprocessing is enabled")

    image = cv2.imread(str(image_path))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]

    if max(height, width) < 1600:
        gray = cv2.resize(
            gray,
            None,
            fx=1.5,
            fy=1.5,
            interpolation=cv2.INTER_CUBIC,
        )

    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )

    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{image_path.stem}-{uuid.uuid4().hex}.png"
    if not cv2.imwrite(str(destination), processed):
        raise OSError(f"Could not write preprocessed image: {destination}")

    return destination
