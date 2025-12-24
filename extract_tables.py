#!/usr/bin/env python3
import pdfplumber
import json
import sys

# Open the PDF
pdf_path = r'c:\Users\Giorgio\Documents\GitHub\Information_retrieval_project\2409.06464v1.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF opened successfully. Total pages: {len(pdf.pages)}\n")
        
        # Extract all tables from the PDF
        all_tables = []
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            if tables:
                for table_idx, table in enumerate(tables):
                    print(f"\n{'='*80}")
                    print(f"TABLE FOUND - Page {page_num}, Table {table_idx + 1}")
                    print(f"{'='*80}")
                    
                    # Print the table in a readable format
                    if table:
                        for row_idx, row in enumerate(table):
                            print(f"Row {row_idx}: {row}")
                    
                    all_tables.append({
                        'page': page_num,
                        'table_index': table_idx + 1,
                        'data': table
                    })
        
        if not all_tables:
            print("No tables found in the PDF. Trying alternative extraction method...")
            # Try to extract text and look for table patterns
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    print(f"\nPage {page_num} text preview:")
                    print(text[:500])

except ImportError:
    print("pdfplumber is not installed. Please install it with: pip install pdfplumber")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
