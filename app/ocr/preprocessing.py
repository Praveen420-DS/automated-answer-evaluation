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


def preprocess_image(path: str | Path, enabled: bool = False) -> Path:
    image_path = validate_image(path)
    if not enabled:
        return image_path

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

    return image_path
