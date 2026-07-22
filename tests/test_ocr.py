from pathlib import Path

from app.ocr.extractor import extract_text_from_image


# Folder containing sample images
SAMPLES_DIR = Path(__file__).parent / "samples"

# Folder to save OCR results
RESULTS_DIR = Path(__file__).parent / "ocr_results"


def main():
    # Create output folder if it does not exist
    RESULTS_DIR.mkdir(exist_ok=True)

    # Supported image formats
    supported_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".webp",
    }

    # Find all images
    image_files = sorted(
        [
            file
            for file in SAMPLES_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower() in supported_extensions
        ]
    )

    if not image_files:
        print("No image files found in tests/samples/")
        return

    print("=" * 60)
    print("           OCR BATCH TEST")
    print("=" * 60)

    print(f"Total images found: {len(image_files)}")
    print()

    successful = 0
    failed = 0

    for index, image_path in enumerate(image_files, start=1):

        print("-" * 60)
        print(f"[{index}/{len(image_files)}] Processing: {image_path.name}")
        print("-" * 60)

        try:
            # Run OCR
            text = extract_text_from_image(str(image_path))

            # Create output filename
            output_file = RESULTS_DIR / f"{image_path.stem}_ocr.txt"

            # Save OCR result
            output_file.write_text(
                text,
                encoding="utf-8"
            )

            print("OCR Status: SUCCESS")
            print(f"Result saved: {output_file}")
            print()
            print("OCR Preview:")
            print(text[:500])

            successful += 1

        except Exception as error:
            print("OCR Status: FAILED")
            print(f"Error: {error}")

            failed += 1

    print()
    print("=" * 60)
    print("                 OCR SUMMARY")
    print("=" * 60)

    print(f"Total images : {len(image_files)}")
    print(f"Successful   : {successful}")
    print(f"Failed       : {failed}")

    print("=" * 60)


if __name__ == "__main__":
    main()