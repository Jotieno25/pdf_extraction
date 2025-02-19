# PDF Data Extraction & Processing

## Overview
This project automates the extraction and processing of tabular data from PDF reports using Python. The script extracts data from structured PDF reports, cleans the extracted information, and organizes it into a usable format.

## Features
- Extracts tabular data from multi-page PDFs.
- Cleans and structures extracted data using Pandas.
- Removes unnecessary headers and redundant text.
- Merges sample data with TVC analysis for better insights.
- Outputs processed data in a structured DataFrame.

## Tech Stack
- **Python**
- **pdfplumber** (for PDF data extraction)
- **Pandas** (for data manipulation)


## Usage
1. Place your PDF file in the project directory.
2. Update the `pdf_path` variable in `main()` with the PDF filename.
3. Run the script:
```bash
python PDF_Extraction.py
```
4. The script will extract and display structured data.

