import os
import pandas as pd

BOOKS_FILE = 'books.csv'

# Add a new book to the database
def books_add(book_data):
    columns = ['cover', 'author', 'title', 'pages', 
               'read', 'reading', 'abandoned', 'planned',
               'notes']
    
    # Replace empty values with empty string
    processed_data = []
    for value in book_data:
        # Check for NaN (special type in pandas)
        if pd.isna(value) or value == 'nan' or value is None:
            processed_data.append('')
        else:
            processed_data.append(str(value))
    
    # Create DataFrame with correct data types
    new_book = pd.DataFrame([processed_data], columns=columns)
    
    # Explicitly convert pages to string
    new_book['pages'] = new_book['pages'].astype(str)
    
    if os.path.exists(BOOKS_FILE):
        # Read existing file, keeping empty strings as empty strings
        existing = pd.read_csv(BOOKS_FILE, dtype=str, keep_default_na=False)
        updated = pd.concat([existing, new_book], ignore_index=True)
    else:
        updated = new_book
    
    # Replace all NaN with empty strings
    updated = updated.fillna('')
    
    updated.to_csv(BOOKS_FILE, index=False)
    print(f"Book added: {processed_data[2]}")

# Fetch all books from the database
def get_books():
    if os.path.exists(BOOKS_FILE):
        # Read all columns as strings, don't convert empty strings to NaN
        df = pd.read_csv(BOOKS_FILE, dtype=str, keep_default_na=False)
        df = df.fillna('')
        return df.to_dict('records')
    return []

# Update a book at the given index
def update_book(index, book_data):
    if os.path.exists(BOOKS_FILE):
        # Read all columns as strings
        df = pd.read_csv(BOOKS_FILE, dtype=str, keep_default_na=False)
        
        if 0 <= index < len(df):
            columns = ['cover', 'author', 'title', 'pages', 
                      'read', 'reading', 'abandoned', 'planned',
                      'notes']
            
            # Process input data
            processed_data = []
            for value in book_data:
                if pd.isna(value) or value == 'nan' or value is None:
                    processed_data.append('')
                else:
                    processed_data.append(str(value))
            
            # Update each column
            for i, col in enumerate(columns):
                df.at[index, col] = processed_data[i]
            
            df = df.fillna('')
            
            df.to_csv(BOOKS_FILE, index=False)
            print(f"Book at index {index} updated")

# Delete a book at the given index
def delete_book(index):
    if os.path.exists(BOOKS_FILE):
        df = pd.read_csv(BOOKS_FILE, dtype=str, keep_default_na=False)
        if 0 <= index < len(df):
            df = df.drop(index).reset_index(drop=True)
            df.to_csv(BOOKS_FILE, index=False)
            print(f"Book at index {index} deleted")