from celery import shared_task
import os
import hashlib
import requests
from bs4 import BeautifulSoup

DOWNLOAD_DIR = "../downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_file_hash(file_path):
    """Compute the hash of the file to compare if it's updated."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@shared_task
def fetch_pdfs():
    websites = [
        "https://www.dgft.gov.in/CP/?opt=ft-policy",
        # Add other URLs to scrape here
    ]

    for url in websites:
        try:
            print(f"Checking for PDFs on {url}...")

            # Scrape the website for PDF links
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links to PDFs
            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
            
            for pdf_link in pdf_links:
                # Construct full PDF URL
                if not pdf_link.startswith("http"):
                    pdf_link = url.rstrip('/') + '/' + pdf_link.lstrip('/')

                # Get the filename from the URL
                pdf_filename = os.path.basename(pdf_link)

                # Check if the PDF already exists in the download folder
                pdf_path = os.path.join(DOWNLOAD_DIR, pdf_filename)

                if os.path.exists(pdf_path):
                    # Compare the hash of the local and remote PDF
                    current_hash = get_file_hash(pdf_path)
                    response = requests.get(pdf_link, stream=True)
                    remote_data = response.content
                    remote_hash = hashlib.md5(remote_data).hexdigest()

                    if current_hash == remote_hash:
                        print(f"PDF {pdf_filename} has not changed. Skipping download.")
                        continue

                # Download the new or updated PDF
                print(f"Downloading {pdf_filename}...")
                response = requests.get(pdf_link)
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"Downloaded {pdf_filename}.")
        
        except Exception as e:
            print(f"Error fetching PDFs from {url}: {str(e)}")
