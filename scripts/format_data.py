import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Color
from openpyxl.formatting.rule import ColorScale, FormatObject

fmt_dict = {
    'Date': {
        'number_format': 'DD/MM/YYYY',
        'alignment': 'right'     
        },
    'Pizza': {
        'alignment': 'left'
    },
    '#': {
        'alignment': 'center'
    },
    'Pizzeria': {
        'alignment': 'left'
    }
}

if __name__ == '__main__':
    # Define paths to input CSV and output Excel file
    csv_path = 'input/data/upload.csv'
    excel_path = 'data/data.xlsx'
    # Load data
    csv_df = pd.read_csv(csv_path)
    csv_columns = [col.strip() for col in csv_df.columns]
    # Validate structure
    required_columns = {'Date', 'Pizza', '#', 'Pizzeria'}
    if not required_columns.issubset(csv_columns):
        raise Exception(f'Missing columns. Required: {required_columns}')
    # Open Excel workbook and sheet
    wb = load_workbook(excel_path)
    ws = wb['Orders']
    # Find max row manually as `ws.max_row` may be incorrect if there are empty rows with some formatting.
    for cell in ws['A']:
        if cell.value is None:
            max_row = cell.row - 1
            break
    # Append rows
    next_row = max_row + 1 # first empty row
    for _, row in csv_df.iterrows():
        for col_idx, value in enumerate(row.tolist(), 1):
            # Set the new cell value
            cell = ws.cell(row=next_row, column=col_idx)
            cell.value=value.strip() if isinstance(value, str) else value
            # Apply formatting based on column
            col_fmt_dict = fmt_dict.get(csv_columns[col_idx-1], {})
            number_format = col_fmt_dict.get('number_format', None)
            if number_format:
                cell.number_format=number_format
            cell.alignment = Alignment(horizontal=col_fmt_dict.get('alignment',
                                                                    'left'))
        next_row += 1
    # Extend the table range
    ws.tables['Orders'].ref = f"A1:D{next_row-1}"
    # Extend the conditional formatting range
    # TODO. Check if there is already a conditional formatting rule and update it. Looking from Excel, the newly appended lines are already included in the existing rules, but are -for some reason- not formatted.
    # Save workbook
    wb.save(excel_path)