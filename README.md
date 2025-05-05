# Bill Analyzer 🧾💡

A smart web-based bill analyzer that extracts key details from uploaded bills or receipts using OCR and Natural Language Processing (NLP). It provides structured outputs like item names, quantities, prices, totals, and purchase dates for better financial tracking and automation.

## 🚀 Features

- 📸 Upload scanned bills or receipts (images or PDFs)
- 🔍 Extracts item names, prices, quantity, date, and total
- 🧠 Uses OCR (EasyOCR / Tesseract) and regex/NLP
- 📊 Displays structured results in table format
- 🌐 Simple web interface for uploading and viewing results

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Libraries & Tools:** EasyOCR, pytesseract, OpenCV, pandas, Flask

## 📁 Project Structure

bill_analyzer/

├── app.py # Flask app

├── analyzer.py # Core bill analysis logic

├── templates/

│ └── index.html # Frontend UI

├── static/

│ └── style.css # CSS styling

├── utils/

│ └── ocr_utils.py # OCR helper functions

├── uploads/ # Uploaded files

├── requirements.txt # Dependencies





## ⚙️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/bill_analyzer.git
   cd bill_analyzer


2. **Install Dependencies**


    pip install -r requirements.txt
   
3. **Install OCR Tools**

  EasyOCR

    
    pip install easyocr
    Tesseract (Optional Alternative)

  Install from here

    Add to PATH (if on Windows)
    
4. **Run the App**


    python app.py
5. **View in Browser**

Visit: http://localhost:5000

**🧾 Supported Input Formats**
    PNG, JPG, JPEG (Image bills)
    
    PDF (if converted to image internally)

**🧪 Example Use Cases**
    Expense tracking
    
    Automating invoice entry
    
    Receipt archiving and analytics

**🙌 Acknowledgements**
    EasyOCR
    
    Tesseract OCR
    
    Flask
    
    OpenCV
