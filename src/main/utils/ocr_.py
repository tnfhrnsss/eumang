import pytesseract
from PIL import Image
import os
import json

from . import util

with open('./main/env.json') as f:
    config = json.load(f)


def extract_text_from_upload(filename):
    image_folder = config['upload_dir']
    text = ''
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        try:
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)
            image = image.convert('L')
            text = pytesseract.image_to_string(image, lang='eng')
            image.close()
            # refine text
            text = util.refine(text)
        except (IOError, OSError) as e:
            print(f"Error: Unable to open image file {filename}. {e}")
        except pytesseract.TesseractError as e:
            print(f"Error: Tesseract OCR failed on image {filename}. {e}")
    return text



def extract_text_from_batch():
    image_folder = config['save_dir']
    extracted_texts = []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            try:
                image_path = os.path.join(image_folder, filename)
                image = Image.open(image_path)
                #image.verify()

                text = pytesseract.image_to_string(image, lang='kor')
                image.close()

                # refine text
                text = util.refine(text)

                extracted_texts.append(text)
            except (IOError, OSError) as e:
                print(f"Error: Unable to open image file {image_path}. {e}")
            except pytesseract.TesseractError as e:
                print(f"Error: Tesseract OCR failed on image {image_path}. {e}")
    print(extracted_texts)
    util.save_to_file(extracted_texts)