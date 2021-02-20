import logging

from PIL import Image
import pytesseract


def recognize(img, lang="eng+chi_sim"):
    """Process a PIL image."""
    extracted = pytesseract.image_to_string(img, lang=lang)

    logging.info(f"Extracted text - {extracted}")

    return extracted

