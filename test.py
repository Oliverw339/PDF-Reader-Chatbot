import PyPDF2 
from PyPDF2 import PdfReader
import sys

from PyPDF2 import PdfReader
from pathlib import Path

pdf_path = (
    Path(__file__).parent /
    "Baking PDFs" /
    "Keto-Breads-Digital-Version_Spreads_Upload (9).pdf"
)

reader = PdfReader(pdf_path)

print(type(reader))
print(type(reader.pages))
print(reader.pages)
