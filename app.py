import cv2
import pytesseract
import re
import os
from preprocess import Preprocess
#pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


UPLOAD_FOLDER = 'static/'
RESULT_FOLDER = 'Results/'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)


fname = None
img_tag = None


def write_to_file(name, email, phone, address):
    txt_fname = RESULT_FOLDER + fname.split('.')[0] + '.csv'
    

    name = name or 'Not Found'
    email = email or 'Not Found'
    phone = phone or 'Not Found'
    address = address or 'Not Found'

    with open(txt_fname, 'w') as f:
        f.write(f'Name, {name}\n')
        f.write(f'Email, {email}\n')
        f.write(f'Phone, {phone}\n')
        f.write(f'Address, {address}\n')


def preprocess_image_for_ocr(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return binary

def upload_image(file_path):
    global fname, img_tag
    

    fname = os.path.basename(file_path)
    img = cv2.imread(file_path)
    

    card = Preprocess(img)
    img = card.detect_card_from_image()


    output_img_path = os.path.join(UPLOAD_FOLDER, fname)
    cv2.imwrite(output_img_path, img)

    img_tag = f'<img src="{output_img_path}" alt="Card Image" class="block shadow-xl rounded-md border border-slate-900 mx-auto w-[300px]">'
    
    return img_tag


def extract_information():
    global fname, img_tag
    if not fname:
        print("No image file uploaded")
        return

    # Load the image
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, fname))

    # Preprocess image for better OCR (e.g., convert to grayscale and threshold)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Extract text with bounding box data
    data = pytesseract.image_to_data(binary, lang='eng', output_type=pytesseract.Output.DICT)

    # Initialize placeholders
    name, email, phone, address = None, None, None, None

    # Step 1: Extract Name (prioritize bold/larger text or central text)
    name_candidates = []
    for i in range(len(data['text'])):
        # Look for bold or large text
        if int(data['conf'][i]) > 60 and int(data['height'][i]) > 20:  # Adjust height threshold
            name_candidates.append(data['text'][i])

    if name_candidates:
        # Join candidates into a potential full name
        name = " ".join(name_candidates)
    else:
        # Fallback to regex-based name detection
        name_match = re.search(
            r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?\b',
            pytesseract.image_to_string(img, lang='eng')
        )
        name = name_match.group(0) if name_match else "Not Found"

    # Step 2: Extract Email
    email = re.findall(r'[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}', pytesseract.image_to_string(img, lang='eng'))
    email = email[0] if email else "Not Found"

    # Step 3: Extract Phone Number
    normalized_text = pytesseract.image_to_string(img, lang='eng').replace("\t", " ").strip()
    phone = re.findall(r'(\+?\d{1,4}[ -]?(\(?\d{1,4}\)?)[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,4})', normalized_text)
    phone = phone[0][0] if phone else "Not Found"

    # Step 4: Extract Address
    text_without_phone = normalized_text.replace(phone, "")
    address_match = re.search(
        r'\d{1,5}[\s.,/()-]?[A-Za-zÀ-ÖØ-öø-ſ,]+(?:[\s.,/()-]?[A-Za-zÀ-ÖØ-öø-ſ]+)*',
        text_without_phone
    )
    address = address_match.group(0).strip() if address_match else "Not Found"

    # Write to results file
    write_to_file(name, email, phone, address)

    return name, email, phone, address, img_tag


if __name__ == '__main__':
    

    
    image_path = 'images/img12.jpg' 
    img_tag = upload_image(image_path)
    print(f"Uploaded image: {img_tag}")


    name, email, phone, address, img_tag = extract_information()
    print(f"Extracted Information:\nName: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}")
    
    