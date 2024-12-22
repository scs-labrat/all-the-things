import os
import re
import pdfplumber
import docx
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich import box
import sys
import time
import shutil
import pyfiglet
import requests
from googlesearch import search

# Initialize rich console with a custom theme
custom_theme = Theme({
    "header": "bold magenta",
    "info": "dim cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
})
console = Console(theme=custom_theme)

# --- Helper Functions for Displaying ASCII Art (Optional) ---
def get_terminal_size():
    """Return the size of the terminal window."""
    columns, lines = shutil.get_terminal_size((80, 20))
    return columns, lines

def read_ascii_art(file_path):
    """Read ASCII art from a file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def display_ascii_art(art, columns):
    """Display ASCII art resized to fit the terminal width."""
    for line in art:
        print((line.strip('\n') + ' ' * columns)[:columns])

def banner():
    """Display banner ASCII art."""
    file_path = 'ascii_art.txt'  # Assuming you have an ASCII art file
    if os.path.exists(file_path):
        ascii_art = read_ascii_art(file_path)
        columns, rows = get_terminal_size()
        os.system('cls' if os.name == 'nt' else 'clear')
        display_ascii_art(ascii_art, columns)
        time.sleep(5)  # Reduced wait time
        print("\033c", end="") # Clear the screen

def title():
    wordart = pyfiglet.figlet_format("ATT", font="dos_rebel")
    print(wordart)


# List of keywords to search for in tables
keywords = [
    'TADIG Code', 'Network Name', 'Network Type', 'Technology', '2G Frequencies', '3G Frequencies',
    '4G Frequencies', '5G Frequencies', 'MSISDN Number Ranges', 'Country Code', 'National Destination Code',
    'SN Range Start', 'SN Range Stop', 'Mobile Country Code', 'Mobile Network Code', 'IMSI to MGT Translation',
    'Does Number Portability Apply?', 'SCCP Gateway Information', 'SCCP Carrier Name', 'DPC Information',
    'XUDT/XUDTS Segmentation Capabilities', 'ANSI Networks SCCP Gateway', 'Subscriber Identity Authentication',
    'Authentication Performed for GSM Subscribers', 'Authentication Performed for GPRS Subscribers', 'Cipher Algorithm',
    'Automatic Roaming Testing', 'AAC (Automatic Answering Circuit) Information',
    'DAAC (Data Automatic Answering Circuit) Information', 'Mobile Application Part (MAP) Information',
    'Application Context Names', 'Inbound Roaming', 'Outbound Roaming', 'MSC/VLR, SGSN versions',
    'MAP Versions', 'MAP Functionality', 'roamingNumberEnquiry', 'subscribeDataMngt', 'CAMEL Information',
    'CAMEL Phases and Versions', 'O-CSI', 'D-CSI', 'MT-SMS-CSI', 'CAP Version', 'CAPv2', 'CAPv3', 'CAPv4',
    'Partial Implementations', 'CAMEL Phase 4 CSIs', 'MG-CSI', 'Network Elements Information', 'Node Types',
    'HLR', 'MSC/VLR', 'SCP', 'SMSC', 'Node IDs and Addresses', 'E.164 Numbers', 'IP Addresses',
    'Global Title Addresses', 'Roamware Dummy Global Titles', 'VIP Information', 'SGSN', 'GGSN VIP IP addresses',
    'Packet Data Services Information', 'APN Identifiers', 'APN Operator Identifier', 'APN Credentials',
    'APN DNS IP Addresses', 'GTP Versions', 'GTPv1', 'SGSN and GGSN Versions', 'Multiple PDP Context Support',
    '2G/3G Data Service Profiles', 'GPRS Information', 'APN List for Testing and Troubleshooting',
    'WAP APN', 'MMS APN Information', 'Pingable and Trace-routable IP Addresses', 'Autonomous System Numbers',
    'ASN', 'GRX Providers', 'Inter-PLMN GSN Backbone IP Address Ranges', 'LTE Roaming Information',
    'IPX Provider Names', 'Primary IP Addresses', 'Secondary IP Addresses', 'Diameter Architecture',
    'EPC Realms for Roaming', 'S6a', 'S6d', 'SMS over NAS Support', 'LTE QoS Profiles', 'Miscellaneous Information',
    'MSRN Structure', 'IMSI Structure', 'SMSC GT Addresses', 'Additional Global Title Addresses', 'Roamware Dummy'
]

def table_contains_keywords(table, keywords):
    for row in table:
        for cell in row:
            if cell:
                for keyword in keywords:
                    if keyword.lower() in cell.lower():
                        return True
    return False

def get_table_keyword(table, keywords):
    """Return the most relevant keyword found in the table."""
    keyword_counts = {}
    for row in table:
        for cell in row:
            if cell:
                for keyword in keywords:
                    if keyword.lower() in cell.lower():
                        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    if keyword_counts:
        # Return the keyword with the highest count
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_keywords[0][0].replace(' ', '_')  # Replace spaces with underscores for filenames
    return 'table'

def extract_tables_from_pdf(file_path, keywords):
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract all tables from the page
            page_tables = page.extract_tables()
            if page_tables:
                for table in page_tables:
                    # Check if table contains any of the keywords
                    if table_contains_keywords(table, keywords):
                        console.print(f"Found matching table on page {page_num} in [info]{os.path.basename(file_path)}[/info]", style="success")
                        tables.append(table)
    return tables

def extract_tables_from_docx(file_path, keywords):
    doc = docx.Document(file_path)
    tables = []
    for table in doc.tables:
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        if data and table_contains_keywords(data, keywords):
            console.print(f"Found matching table in [info]{os.path.basename(file_path)}[/info]", style="success")
            tables.append(data)
    return tables

def save_tables(tables, output_directory, base_filename):
    for i, table in enumerate(tables):
        # Standardize the table rows
        max_columns = max(len(row) for row in table)
        standardized_table = []
        for row in table:
            # Pad rows with fewer columns
            if len(row) < max_columns:
                row.extend([''] * (max_columns - len(row)))
            elif len(row) > max_columns:
                row = row[:max_columns]
            standardized_table.append(row)
        # Use the first row as the header
        header = standardized_table[0]
        data_rows = standardized_table[1:]
        # Replace empty headers with default names
        header = [f"Column_{j+1}" if not col else col for j, col in enumerate(header)]
        # Create the DataFrame
        df = pd.DataFrame(data_rows, columns=header)
        # Get a keyword for the table name
        table_keyword = get_table_keyword(standardized_table, keywords)
        # Ensure table_keyword is valid for filenames
        table_keyword = re.sub(r'[^\w\-_. ]', '_', table_keyword)
        # Save the DataFrame to CSV
        output_file = os.path.join(output_directory, f"{base_filename}_{table_keyword}_{i+1}.csv")
        df.to_csv(output_file, index=False)
        console.print(f"Saved table to [success]{output_file}[/success]")

def display_tables_from_folder(output_directory, selected_indices=None):
    # List CSV files in the directory
    csv_files = [f for f in os.listdir(output_directory) if f.endswith('.csv')]
    if not csv_files:
        console.print("No tables found in this folder.", style="warning")
        return
    if selected_indices is None:
        selected_indices = range(1, len(csv_files) + 1)
    for idx in selected_indices:
        if 1 <= idx <= len(csv_files):
            csv_file = csv_files[idx - 1]
            df = pd.read_csv(os.path.join(output_directory, csv_file))
            console.print(f"Displaying [info]{csv_file}[/info]:", style="header")
            display_table_with_rich(df)
        else:
            console.print(f"Table number {idx} is out of range.", style="error")

def display_table_with_rich(df):
    # Create a rich Table instance
    table = Table(show_header=True, header_style="bold magenta", box=box.SQUARE)

    # Add columns to the table
    for column in df.columns:
        table.add_column(str(column), overflow="fold")

    # Add rows to the table
    for index, row in df.iterrows():
        table.add_row(*[str(item) for item in row])

    # Render the table using the console
    console.print(table)

def process_file(file_path, directory):
    filename = os.path.basename(file_path)
    console.print(f"Processing file: [info]{filename}[/info]", style="success")
    if filename.lower().endswith(".pdf"):
        tables = extract_tables_from_pdf(file_path, keywords)
    elif filename.lower().endswith(".docx"):
        tables = extract_tables_from_docx(file_path, keywords)
    else:
        console.print(f"Skipping file: [warning]{filename}[/warning] (unsupported format)")
        return

    if tables:
        # Create a folder named after the file name (without extension)
        base_filename = os.path.splitext(filename)[0]
        output_directory = os.path.join(directory, base_filename)
        os.makedirs(output_directory, exist_ok=True)
        save_tables(tables, output_directory, base_filename)
        display_tables_from_folder(output_directory)
    else:
        console.print(f"No matching tables found in [warning]{filename}[/warning]", style="warning")

def list_processed_folders(directory):
    # List all directories in the specified directory
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    # Exclude hidden folders and system directories
    folders = [f for f in folders if not f.startswith('.')]
    if not folders:
        console.print("No previously ingested folders found.", style="warning")
        return []
    console.print("Previously ingested folders:", style="header")
    for idx, folder in enumerate(folders, 1):
        console.print(f"{idx}. {folder}")
    return folders

def parse_user_selection(user_input, max_value):
    selections = set()
    parts = user_input.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range
            try:
                start_str, end_str = part.split('-')
                start = int(start_str)
                end = int(end_str)
                if start <= end:
                    for i in range(start, end + 1):
                        if 1 <= i <= max_value:
                            selections.add(i)
                else:
                    console.print(f"Invalid range '{part}'.", style="error")
            except ValueError:
                console.print(f"Invalid range '{part}'.", style="error")
        else:
            # Single number
            try:
                i = int(part)
                if 1 <= i <= max_value:
                    selections.add(i)
                else:
                    console.print(f"Invalid number '{part}'.", style="error")
            except ValueError:
                console.print(f"Invalid input '{part}'.", style="error")
    return sorted(selections)

def parse_directory_input(directory_input):
    # Remove quotes if present
    directory = directory_input.strip('"\'')
    # Remove anything after the last '/' or '\'
    if '/' in directory:
        directory = directory.rsplit('/', 1)[0]
    elif '\\' in directory:
        directory = directory.rsplit('\\', 1)[0]
    return directory

def read_recent_directories():
    recent_dirs = []
    if os.path.exists('recent_dirs.txt'):
        with open('recent_dirs.txt', 'r') as file:
            recent_dirs = [line.strip() for line in file.readlines()]
    return recent_dirs[:3]

def write_recent_directory(directory):
    recent_dirs = read_recent_directories()
    if directory in recent_dirs:
        recent_dirs.remove(directory)
    recent_dirs.insert(0, directory)
    with open('recent_dirs.txt', 'w') as file:
        for dir in recent_dirs[:3]:
            file.write(dir + '\n')

def recall_tables():
    print("\033c", end="")
    title()
    recent_dirs = read_recent_directories()
    if recent_dirs:
        console.print("Recent directories:", style="header")
        for idx, dir in enumerate(recent_dirs, 1):
            console.print(f"{idx}. {dir}")
    console.print("Enter the base directory where ingested folders are stored:")
    base_dir_input = console.input("(You can select a recent directory by number, or enter a new path): ").strip()
    if base_dir_input.isdigit():
        selection = int(base_dir_input)
        if 1 <= selection <= len(recent_dirs):
            directory = recent_dirs[selection - 1]
        else:
            console.print("Invalid selection.", style="error")
            return
    else:
        directory = parse_directory_input(base_dir_input)
    if os.path.isdir(directory):
        write_recent_directory(directory)
        folders = list_processed_folders(directory)
        if not folders:
            return
        try:
            choice = int(console.input("Select a folder number to display tables (0 to cancel): "))
        except ValueError:
            console.print("Invalid input.", style="error")
            return
        if choice == 0:
            return
        if 1 <= choice <= len(folders):
            selected_folder = folders[choice - 1]
            output_directory = os.path.join(directory, selected_folder)
            # Now list the tables in the folder
            csv_files = [f for f in os.listdir(output_directory) if f.endswith('.csv')]
            if not csv_files:
                console.print("No tables found in this folder.", style="warning")
                return
            # Display the list of tables with numbers and titles
            console.print("Available tables in the folder:", style="header")
            for idx, csv_file in enumerate(csv_files, 1):
                console.print(f"{idx}. {csv_file}")
            while True:
                user_input = console.input("Enter table numbers to display (e.g., 1,2-5,8), or 0 to go back: ")
                if user_input.strip() == '0':
                    return
                selected_indices = parse_user_selection(user_input, len(csv_files))
                if selected_indices:
                    # Display selected tables
                    display_tables_from_folder(output_directory, selected_indices)
                    # Ask if they want to view more
                    more_input = console.input("Would you like to view more tables from this folder? (y/n): ").strip().lower()
                    if more_input != 'y':
                        return
                else:
                    console.print("No valid table numbers entered. Please try again.", style="error")
        else:
            console.print("Invalid selection.", style="error")
    else:
        console.print("Invalid directory. Please try again.", style="error")

def explain_tool():
    console.print("\n[+] What is this tool?", style="header")

    # Explain the purpose of the tool
    console.print("\nThis tool is designed to extract, parse, and display important telecom data from GSMA IR.21 forms.")
    console.print("GSMA IR.21 forms are documents used by mobile operators to exchange important network details "
                  "that are required for international roaming, including details about frequency bands, "
                  "roaming agreements, and network node information.")

    # Explain how to find IR.21 PDFs using Google Dorking
    console.print("\n[+] How to find GSMA IR.21 PDFs using Google Dorking:")
    console.print("Google Dorking is a technique that uses advanced search queries to find specific documents.")
    console.print("To find IR.21 forms, you can use the following Google search query:")
    console.print("[green]\"site:example.com filetype:pdf IR.21\"[/green]")
    console.print("Replace [bold]example.com[/bold] with the target domain or remove it to search across all domains. "
                  "You can also use keywords like [bold]\"GSMA IR.21\"[/bold] to narrow down your search.")

    # Explain how to place IR.21 files in a folder
    console.print("\n[+] How to prepare the documents:")
    console.print("Once you've found GSMA IR.21 PDFs using Google Dorking or from other sources, "
                  "download them and place them all into a single folder on your computer.")
    
    # Explain how to import the files into the tool
    console.print("\n[+] Importing the documents into All-the-things:")
    console.print("1. Use the [bold]\"Process new documents\"[/bold] option in the main menu.")
    console.print("2. Enter the directory path where you stored the IR.21 files.")
    console.print("3. The tool will automatically process each document, extract tables, and save the results.")
    console.print("4. You can then use the [bold]\"Recall tables\"[/bold] option to view or export the data.")

    console.print("\nThis tool automates the extraction of valuable information from telecom documents, making it easier "
                  "for network engineers and cybersecurity professionals to analyze and manage telecom data.")

def google_dork_ir21():
    console.print("\n[+] Performing Google Dork search for IR.21 PDFs...", style="header")

    # Define the Google Dork query for IR.21 PDFs
    query = "filetype:pdf IR.21"

    # Perform the Google search
    search_results = []
    try:
        # Use only the required arguments
        for result in search(query, num_results=10):
            search_results.append(result)
    except Exception as e:
        console.print(f"[error]Error while performing Google search: {e}[/error]")
        return

    # Check if any results were found
    if not search_results:
        console.print("[warning]No results found for IR.21 PDFs[/warning]")
        return

    # Display the found URLs
    console.print("\n[+] Found the following IR.21 PDF links:", style="header")
    for idx, link in enumerate(search_results, 1):
        console.print(f"{idx}. {link}")

    # Prompt the user to select a link to download
    while True:
        try:
            choice = int(console.input("\nEnter the number of the PDF you want to download (or 0 to cancel): ").strip())
            if choice == 0:
                return
            elif 1 <= choice <= len(search_results):
                selected_link = search_results[choice - 1]
                download_pdf(selected_link)
                return
            else:
                console.print("[error]Invalid selection. Please choose a valid number from the list.[/error]")
        except ValueError:
            console.print("[error]Invalid input. Please enter a number.[/error]")


def download_pdf(url):
    # Define the directory to save the PDFs
    save_dir = "./my_ir21"
    os.makedirs(save_dir, exist_ok=True)

    # Extract the file name from the URL
    file_name = url.split("/")[-1]
    file_path = os.path.join(save_dir, file_name)

    console.print(f"\n[+] Downloading PDF from {url}...", style="info")

    try:
        # Perform the download
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Write the file to disk
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

        console.print(f"[success]Downloaded PDF to: {file_path}[/success]")
    except Exception as e:
        console.print(f"[error]Failed to download PDF: {e}[/error]")


def main_menu():
    banner()
    title()
    console.print("\n[+] Welcome to All-the-things!", style="header")
    while True:
        console.print("\nPlease choose an option:")
        console.print("1. Process new documents")
        console.print("2. Recall tables from previously ingested folders")
        console.print("3. What does this tool do?")
        console.print("4. Perform Google Dork for IR.21 PDFs")
        console.print("5. Exit")
        choice = console.input("Enter your choice (1-5): ")
        if choice == '1':
            directory_input = console.input("Enter the directory path containing the documents: ").strip()
            directory = parse_directory_input(directory_input)
            if os.path.isdir(directory):
                files = [os.path.join(directory, f) for f in os.listdir(directory)]
                for file_path in files:
                    process_file(file_path, directory)
                write_recent_directory(directory)
            else:
                console.print("Invalid directory. Please try again.", style="error")
        elif choice == '2':
            recall_tables()
        elif choice == '3':
            explain_tool()
        elif choice == '4':
            google_dork_ir21()
        elif choice == '5':
            console.print("Goodbye!", style="success")
            sys.exit(0)
        else:
            console.print("Invalid choice. Please try again.", style="error")



if __name__ == "__main__":
    main_menu()
