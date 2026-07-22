import re
import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)


class QuestionParser:

    def __init__(self):
        pass

    # -------------------------
    # Extract Text from Image
    # -------------------------

    def extract_text(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Question paper not found.")

        result = reader.readtext(image)

        text = ""

        for item in result:
            text += item[1] + "\n"

        return text

    # -------------------------
    # Parse Questions
    # -------------------------

    def parse_questions(self, text):

        pattern = r"(Q\d+\.?|[0-9]+\.)"

        matches = list(re.finditer(pattern, text))

        questions = []

        for i in range(len(matches)):

            start = matches[i].start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            question_text = text[start:end].strip()

            mark_match = re.search(r"\((\d+)\s*Marks?\)", question_text)

            marks = 0

            if mark_match:
                marks = int(mark_match.group(1))

            questions.append({

                "questionNumber": i + 1,

                "question": question_text,

                "marks": marks

            })

        return questions


question_parser = QuestionParser()