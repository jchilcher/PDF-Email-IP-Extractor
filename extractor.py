import os
import fitz
import re
import csv

# Path to the directory containing PDF files
pdf_directory = os.getcwd()

# Initialize CSV writer
csv_file = "output.csv"
csv_header = ["Email Address", "IP Address", "Source File"]
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

# Function to extract email addresses and IP addresses using regex
def extract_addresses(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    emails = re.findall(email_pattern, text)
    ips = re.findall(ip_pattern, text)
    return emails, ips

# Function to process a single PDF file
def process_pdf(pdf_file):
    text = ""
    with fitz.open(pdf_file) as pdf:
        for page in pdf:
            text += page.get_text()
    emails, ips = extract_addresses(text)
    for i in range(max(len(emails), len(ips))):
        email = emails[i] if i < len(emails) else ""
        ip = ips[i] if i < len(ips) else ""
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, ip, os.path.basename(pdf_file)])

# Process all PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_file = os.path.join(pdf_directory, filename)
        process_pdf(pdf_file)