from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from app.ocr.extractor import extract_text_from_image
from app.core.answer_parser import parse_answers


router = APIRouter(
    prefix="/api",
    tags=["Answer Sheet"]
)


UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_answer_sheet(
    file: UploadFile = File(...)
):
    """
    Upload an answer sheet image,
    extract text using OCR,
    and parse questions and answers.
    """

    # Allowed file types
    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf"
    }

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG, and PDF files are supported."
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / unique_filename

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Currently OCR image processing
        # PDF support can be connected separately
        if file_extension == ".pdf":
            raise HTTPException(
                status_code=501,
                detail="PDF OCR processing will be added next."
            )

        # Extract text using OCR
        extracted_text = extract_text_from_image(
            str(file_path)
        )

        # Parse questions and answers
        parsed_answers = parse_answers(
            extracted_text
        )

        return {
            "success": True,
            "filename": file.filename,
            "questions_count": len(parsed_answers),
            "questions": parsed_answers
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

    finally:

        # Delete temporary file
        if file_path.exists():
            file_path.unlink()