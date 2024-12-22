
# 🛠️ **All-the-things** - Telecom IR.21 Extractor

All-the-things is a powerful Python-based tool designed to **automate the extraction, parsing, and analysis of telecom data** from **GSMA IR.21** forms. These forms are used by telecom operators to exchange critical network details required for **international roaming**, making this tool indispensable for **network engineers**, **telecom analysts**, and **cybersecurity professionals**.

---
## 🌟 **Features**

- **Google Dorking for IR.21 PDFs**: Perform advanced Google searches for IR.21 documents, download and process them.
- **Automated Table Extraction**: Extracts telecom-related tables from both **PDF** and **Word** (`.docx`) documents.
- **Data Analysis**: Analyze and manage information like network frequencies, node types, MSISDN number ranges, and roaming details.
- **CSV Export**: Automatically saves extracted data to **CSV** files for further analysis.
- **Rich Interactive Interface**: An elegant terminal interface using **Rich** for displaying tables and processing logs.
  
---

## 🚀 **Getting Started**

### Prerequisites

Before using the tool, make sure you have the following installed:

- **Python 3.7+**
- Required Python packages (install them using the command below):

```bash
pip install -r requirements.txt
```

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/all-the-things.git
cd all-the-things
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Create the directory for storing PDFs**:

```bash
mkdir my_ir21
```

---

## 📖 **Usage**

### Main Menu Options

When you run the tool, you will be presented with the following menu:

1. **Process new documents**: Parse IR.21 files (PDFs or DOCX) from a specified directory and extract telecom tables.
2. **Recall tables from previously ingested folders**: Review and display tables previously extracted from documents.
3. **What does this tool do?**: Learn more about GSMA IR.21 forms, how to find them using Google Dorking, and how to process them using the tool.
4. **Perform Google Dork for IR.21 PDFs**: Automatically perform a Google Dork search to find IR.21 PDF files, download them, and store them in `./my_ir21`.
5. **Exit**: Exit the tool.

### How to Run the Tool

```bash
python all_the_things.py
```

### Example

1. Select **Process new documents** from the main menu.
2. Provide the directory path where your **IR.21 PDF** or **DOCX** files are stored.
3. The tool will extract relevant tables and store them as **CSV** files in a folder named after the document.
4. Use **Recall tables from previously ingested folders** to view the extracted data directly in the terminal.

---

## 🌐 **Performing a Google Dork Search**

To find **IR.21** forms using Google Dorking, follow these steps:

1. Select **Perform Google Dork for IR.21 PDFs** from the main menu.
2. The tool will display a list of found PDF links.
3. Select one to download, and the file will be saved to `./my_ir21` directory.
   
> 💡 _Use Google Dorking carefully and ethically!_

---

## 🛠️ **Customization**

Feel free to modify the tool to meet your specific needs! You can easily extend functionality, add new document formats, or integrate with other data sources.

---

## 📁 **Directory Structure**

Here's a basic overview of the repository structure:

```
all-the-things/
│
├── my_ir21/                       # Directory to store downloaded IR.21 PDFs
├── README.md                      # Project readme
├── requirements.txt               # Dependencies for the project
├── all_the_things.py              # Main tool script
├── recent_dirs.txt                # Tracks recent directories used
└── .gitignore                     # Gitignore file for the project
```

---

## 🧩 **Dependencies**

- **pdfplumber**: For extracting tables from PDF files.
- **python-docx**: For extracting tables from Word (.docx) documents.
- **requests**: For downloading PDFs from the web.
- **googlesearch-python**: For performing Google Dork searches.
- **rich**: For a beautiful, interactive terminal interface.

### Installing dependencies

You can install the required libraries using:

```bash
pip install -r requirements.txt
```

---

## 📊 **CSV Data Example**

Each document's extracted data is saved in a `CSV` file with the document's name. Here is an example of what the extracted data looks like:

| Column 1          | Column 2          | Column 3          | Column 4  |
|-------------------|-------------------|-------------------|-----------|
| TADIG Code        | Network Name       | 4G Frequencies    | APN List  |
| 23430             | Vodafone UK        | 1800MHz, 2600MHz  | vodafone  |
| 310260            | T-Mobile USA       | 1700MHz, 1900MHz  | t-mobile  |

---
---

## 🎉 **Acknowledgements**

- **Rich**: For providing a beautiful terminal UI experience.
- **pdfplumber** and **python-docx**: For document parsing capabilities.
- **Google Search API**: For enabling efficient Google Dorking functionality.

---

## 💡 **Disclaimer**

This tool is designed for educational purposes only. Please ensure that you have permission to download and analyze any IR.21 files, and always adhere to ethical guidelines when using Google Dorking techniques.
