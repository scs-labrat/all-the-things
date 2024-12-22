# All-the-Things Tool

**All-the-Things** is a Python-based tool designed to automate the extraction, parsing, and analysis of key telecom data from GSMA IR.21 forms. It simplifies the process of identifying, organizing, and exporting important information for cybersecurity professionals, network engineers, and telecom analysts.

## Features
- Extracts and parses tables from GSMA IR.21 forms (PDF and DOCX formats).
- Identifies key telecom data such as TADIG codes, frequencies, roaming agreements, and IP addresses.
- Saves parsed tables into structured CSV files.
- Provides a user-friendly interface with support for ASCII art banners and rich-text output.
- Automates Google Dork searches to locate relevant GSMA IR.21 PDFs.
- Supports recalling and displaying previously ingested documents.

## Requirements
### Python Libraries
Ensure the following Python libraries are installed:
- `os`
- `re`
- `pdfplumber`
- `docx`
- `pandas`
- `rich`
- `sys`
- `shutil`
- `pyfiglet`
- `requests`
- `googlesearch`

Install these dependencies using pip:
```bash
pip install pdfplumber python-docx pandas rich pyfiglet requests googlesearch-python
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd all-the-things
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `thethings` directory is present in your project and properly imported.  This contains the included IR21s 
   which must be imported with options 1.

4. Run the tool:
   ```bash
   python all-the-things.py
   ```

## Usage
### Main Menu Options
- **1. Process new documents**: Extract and save tables from GSMA IR.21 forms.
- **2. Recall tables from previously ingested folders**: View or export tables processed earlier.
- **3. What does this tool do?**: Learn about the tool's purpose and capabilities.
- **4. Perform Google Dork for IR.21 PDFs**: Automate searches for GSMA IR.21 documents using Google Dork queries.
- **5. Exit**: Quit the tool.

### Example Workflow
1. Place GSMA IR.21 forms in a directory.
2. Select option `1` and provide the directory path.
3. View the extracted tables, saved as CSV files in the same directory.
4. Use option `2` to recall and display processed tables.
5. Use option `4` to search for additional IR.21 PDFs.

## Key Functions
### Google Dork Search
Automates searching for IR.21 PDFs using a Google Dork query.

### Document Processing
- Extracts tables from PDFs and DOCX files.
- Filters tables based on keywords for relevance.
- Saves tables into well-structured CSV files.

### Recall Processed Tables
Allows viewing and reanalyzing previously processed documents.

## Known Issues
- Google Dorking results may be limited due to search engine restrictions.
- Processing may be slower for large PDFs or DOCX files with complex formatting.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed information about your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


