import os
from dotenv import load_dotenv

load_dotenv()


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    if len(texts) > 0:
        license_plates = []
        license_plate_texts = texts[0].description.split('\n')

        for text in license_plate_texts:
            if len(text) > 3:
                if len(text) <= 9:
                    license_plates.append(text)

        return license_plates

    return None
