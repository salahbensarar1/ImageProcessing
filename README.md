# Business Card Information Extractor

The Business Card Information Extractor is a Python-based application that automates the extraction of structured information from business card images. It uses Optical Character Recognition (OCR) to identify and retrieve details such as Name, Title, Email, Phone Number, Address, and Website. The application preprocesses the input images to improve text recognition and saves the extracted information in CSV files for further use. It handles business cards with different layouts, orientations, and backgrounds, supports embossed or golden text styles, and processes both typed and partially handwritten text.

## Features
- Processes business cards with various designs and text styles.
- Detects and extracts multi-line addresses and phone numbers.
- Supports golden/embossed text using advanced preprocessing techniques.
- Saves processed images for verification and outputs results in `.csv` format.

## Directory Structure
 ```plaintext
.
├── Results/                # Extracted information saved as .csv and .txt files
├── __pycache__/            # Compiled Python files for caching
├── app.py                  # Main script for running the application
├── preprocess.py           # Script for image preprocessing and card detection
├── images/                 # Folder containing input business card images
├── static/                 # Folder for processed images
├── requirements.txt        # List of dependencies
 ```

## Installation
### 1. Clone the repository:
```bash
git clone https://github.com/salahbensarar1/ImageProcessing.git
cd ImageProcessing
```

### 2.	Install dependencies:
```bash
pip install -r requirements.txt

```

### 	3.	Install Tesseract OCR:
####      •	macOS: brew install tesseract
####      •	Ubuntu: sudo apt install tesseract-ocr
####      •	Windows:  <a href="https://github.com/tesseract-ocr/tesseract">Download Tesseract</a>.

### 4.	Update the Tesseract path in app.py:

```python
pytesseract.pytesseract.tesseract_cmd = '<path_to_tesseract>'
```

## Usage
#### 1.	Place your business card images in the images/ directory.
#### 2.	Run the application:
```bash
python app.py
python3 app.py
```
#### 3.	Processed images will be saved in the static/ folder, and extracted information will be stored in .csv or .txt files in the Results/ folder.

## How It Works

#### The preprocess.py script processes input images by resizing large images, enhancing contrast using CLAHE, detecting card regions via contour-based segmentation, and applying adaptive thresholding for OCR optimization. The app.py script extracts text using Tesseract OCR and uses regex patterns to extract names, emails, phone numbers, and addresses. The extracted data is then saved in the Results/ folder as .csv files for easy access.

### Example Outputs

#### A sample business img11.jpg card placed in the images/ folder.
![Business Card Example](https://raw.githubusercontent.com/salahbensarar1/ImageProcessing/main/static/img11.jpg)
#### Extracted CSV Output

```
Name, Zsolt Csaba Johanyak
Email, johanyak.csaba@nje.hu
Phone, +36 20 2508260
Address, 6000 Kecskemét, Izsaki Ut
```

#### Extracted TXT Output

```
Name: Zsolt Csaba Johanyak
Email: johanyak.csaba@nje.hu
Phone: +36 20 2508260
Address: 6000 Kecskemét, Izsaki Ut
```

## Contributing

#### Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.

#### License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, reach out to

[![Salah Ben Sarar](https://cdn.jsdelivr.net/gh/alohe/avatars/png/memo_23.png)](https://github.com/salahbensarar1)


 
