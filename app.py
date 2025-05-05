from flask import Flask, render_template, request, redirect, session, send_file
import os
import fitz  # PyMuPDF
import pandas as pd
from datetime import datetime
import re
import zipfile
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Helper function to extract text from PDF
def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Helper function to parse bill data from text
def parse_bill_data(text):
    invoice_match = re.search(r'Invoice Number:\s*(\S+)', text)
    invoice_number = invoice_match.group(1) if invoice_match else 'Not Found'

    date_match = re.search(r'Date:\s*([\d\-\/]+)', text)
    date = date_match.group(1) if date_match else 'Not Found'

    total_match = re.search(r'Total:\s*([\d\.]+)', text)
    total_price = total_match.group(1) if total_match else '0.00'

    vendor_match = re.search(r'Vendor:\s*(.+)', text)
    vendor_name = vendor_match.group(1) if vendor_match else 'Unknown'

    return {
        'Name': vendor_name,
        'Date': date,
        'Total Price': total_price,
        'Invoice Number': invoice_number
    }

@app.route('/')
def index():
    bill_data = session.get('bill_data', [])
    excel_path = session.get('excel_file_path')

    if excel_path and os.path.exists(excel_path):
        try:
            existing_df = pd.read_excel(excel_path)
            excel_data = existing_df.to_dict(orient='records')
        except Exception:
            excel_data = []
    else:
        excel_data = []

    combined_data = excel_data + bill_data
    return render_template('index.html', bill_data=combined_data)

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files.get('excel_file')
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        session['excel_file_path'] = filepath
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('bill')
    if not file:
        return redirect('/')

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    data = parse_bill_data(text)

    bill_data = session.get('bill_data', [])
    bill_data.append(data)
    session['bill_data'] = bill_data

    return redirect('/')

@app.route('/generate_excel')
def generate_excel():
    bill_data = session.get('bill_data', [])
    if not bill_data:
        return redirect('/')

    # Create DataFrame from PDF data
    pdf_df = pd.DataFrame(bill_data)
    pdf_df['Total Price'] = pd.to_numeric(pdf_df['Total Price'], errors='coerce').fillna(0)

    # Load existing Excel data if available
    excel_path = session.get('excel_file_path')
    if excel_path and os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        existing_df['Total Price'] = pd.to_numeric(existing_df['Total Price'], errors='coerce').fillna(0)
    else:
        existing_df = pd.DataFrame(columns=['Name', 'Date', 'Total Price', 'Invoice Number'])

    # Combine both datasets
    detailed_df = pd.concat([existing_df, pdf_df], ignore_index=True)

    # Create summary
    summary_df = detailed_df.groupby('Name', as_index=False)['Total Price'].sum()

    # Save to temp files in memory
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        detailed_path = 'bill_details.xlsx'
        summary_path = 'bill_summary.xlsx'

        detailed_stream = BytesIO()
        detailed_df.to_excel(detailed_stream, index=False)
        zf.writestr(detailed_path, detailed_stream.getvalue())

        summary_stream = BytesIO()
        summary_df.to_excel(summary_stream, index=False)
        zf.writestr(summary_path, summary_stream.getvalue())

    memory_file.seek(0)
    return send_file(memory_file, download_name='bills_export.zip', as_attachment=True)

@app.route('/clear')
def clear():
    session.pop('bill_data', None)
    session.pop('excel_file_path', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
