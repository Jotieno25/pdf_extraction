import pdfplumber
import pandas as pd

def process_pdf(pdf_path: str) -> pd.DataFrame:
    """
    Extracts data from the given PDF file, processes the tables, and returns a combined DataFrame.
    """
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Skip the first table on each page (assumed not needed)
            tables = page.extract_tables()[1:]
            if tables:
                for table in tables:
                    for row in table:
                        # Append the row if it contains any non-empty cell (after stripping)
                        if any(cell.strip() for cell in row if cell):
                            data.append(row)

    # Define headers that need to be removed from the data
    headers_to_remove = [
        'Time Taken*', 'Temperature at Sampling (°C)*', 'ClO2 at Sampling (mg/l)*',
        'Pseudomonas aeruginosa', 'cfu/ml', 'cfu/100ml', 'Analysis', 'Units', 'Method',
        'MM-015', 'MM-006', 'MM-002A', 'MM-002B', 'MM-005', 'Escherichia coli',
        'Enterococci', 'Coliforms'
    ]

    # Remove any None values and split string cells on newline characters
    data = [[item for item in sublist if item is not None] for sublist in data]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if isinstance(data[i][j], str):
                data[i][j] = data[i][j].split('\n')

    # Remove unwanted header values from each split cell
    for sublist in data:
        for i in range(len(sublist)):
            sublist[i] = [item for item in sublist[i] if item not in headers_to_remove]

    # Extract sample data starting at 'Lab Sample No.'
    sample_data = []
    for entry in data:
        if entry and 'Lab Sample No.' in entry[0]:
            sample_data.append(entry)

    # Extract TVC analysis data
    tvc_22_data = []
    tvc_37_data = []
    for entry in data:
        if entry and 'TVC at 22°C (3 day)' in entry[0]:
            # Assuming the values are in the 4th and 5th columns (indices 3 and 4)
            tvc_22_data.append(entry[3][0])
            tvc_22_data.append(entry[4][0])
        elif entry and 'TVC at 37°C (2 day)' in entry[0]:
            tvc_37_data.append(entry[3][0])
            tvc_37_data.append(entry[4][0])

    # Create a DataFrame for the TVC analysis data
    analysis_restructured = {
        'TVC at 22°C (3 day)': tvc_22_data,
        'TVC at 37°C (2 day)': tvc_37_data
    }
    df_analysis = pd.DataFrame(analysis_restructured)

    # Flatten the sample data (skip header row from each sublist)
    flattened_data = []
    for sublist in sample_data:
        flattened_data.extend(sublist[1:])

    # Define column names for the sample data DataFrame
    columns = ['Lab Sample No.', 'Sample Deviations', 'Sample Type', 'Matrix', 'Other ID*', 'Sample ID']
    df_samples = pd.DataFrame(flattened_data, columns=columns)

    # Combine both DataFrames side by side
    df_combined = pd.concat([df_samples, df_analysis], axis=1)
    return df_combined

def main():
    pdf_path = "J23235-Dolphin Sq-Rodney -Beatty house- Domestic sample report-Combined.pdf"
    df_combined = process_pdf(pdf_path)
    # Display the first 21 rows of the combined DataFrame
    print(df_combined.head(21))

if __name__ == "__main__":
    main()
