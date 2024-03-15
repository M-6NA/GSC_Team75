import pandas as pd
import os


# ::::::::: READING THE DATAFRAME ALSO PREPROCSSING IT :::::::::::

# ::::::::: FINANCE DATA :::::::::
def load_and_process_finance_data():

    RAW_FINANCE_DF = pd.read_excel('data/FinanceReport_r1.xlsx')

    # Function to rename duplicates. For each duplicate, it appends an underscore and a counter to the name.
    def rename_duplicates( old_columns ):
        counts = {}
        new_columns = []
        for col in old_columns:
            if col in counts:
                counts[col] += 1
                new_name = f"{col}_{counts[col]}"
                new_columns.append(new_name)
            else:
                counts[col] = 0
                new_columns.append(col)
        return new_columns

    # Duplicate columns in Finance Report (count):
    # - Operating profit - Indirect cost - Handling costs - Permanent employees (2)
    # - Operating profit - Indirect cost - Handling costs - Flexible manpower (2)
    # - Operating profit - Indirect cost - Administration costs - Order lines (2)
    # - Operating profit - Indirect cost - Administration costs - Orders (2)

    base_names = [
        "Operating profit - Indirect cost - Handling costs - Permanent employees",
        "Operating profit - Indirect cost - Handling costs - Flexible manpower",
        "Operating profit - Indirect cost - Administration costs - Order lines",
        "Operating profit - Indirect cost - Administration costs - Orders"
    ]

    # Function to add suffixes to specific columns
    def add_specific_inbound_outbound_suffixes(columns):
        new_columns = []
        for col in columns:
            # Check if the base of the column name (without '_1' if it exists) is in the list of base names
            base_col = col.replace('_1', '')
            if base_col in base_names:
                # If the original column name ends with '_1', add ' (Outbound)'
                if col.endswith("_1"):
                    new_columns.append(base_col + " (Outbound)")
                # Otherwise, if it doesn't have '_1', add ' (Inbound)'
                else:
                    new_columns.append(col + " (Inbound)")
            else:
                # If the column is not one of the specified columns, leave it as is
                new_columns.append(col)
        return new_columns

    PROCESSED_FINANCE_DF = RAW_FINANCE_DF.copy().T.reset_index()
    PROCESSED_FINANCE_DF.columns = PROCESSED_FINANCE_DF.iloc[0]
    PROCESSED_FINANCE_DF = PROCESSED_FINANCE_DF.drop(PROCESSED_FINANCE_DF.index[0])
    PROCESSED_FINANCE_DF.reset_index(drop = True, inplace = True)
    PROCESSED_FINANCE_DF.columns = rename_duplicates(PROCESSED_FINANCE_DF.columns)
    PROCESSED_FINANCE_DF.columns = add_specific_inbound_outbound_suffixes(PROCESSED_FINANCE_DF.columns)
    PROCESSED_FINANCE_DF.rename(columns = {"Unnamed: 0": "Round"}, inplace = True)

    return RAW_FINANCE_DF, PROCESSED_FINANCE_DF

# ::::::::: SUPPLIERS DATA :::::::::
def load_suppliers_data():

    MANUAL_SUPPLIER_DF = pd.read_excel('data/Suppliers_NEW.xlsx')

    return MANUAL_SUPPLIER_DF

# ::::::::: MAIN DATA :::::::::
def read_main_table_tabs(tab_name):
    MAIN_DATA_DIR = 'data/TFC_MAIN_DATA_R-2to1.xlsx'
    
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = tab_name)

    return tab_df 