from PIL import Image
import pytesseract


# def recognize(img, lang="eng+chi_sim"):
def recognize(img, lang="eng"):
    """Process a PIL image."""
    extracted = pytesseract.image_to_string(img, lang=lang)
    return extracted

