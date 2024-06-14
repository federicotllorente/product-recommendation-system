import pandas as pd
import numpy as np
import json

def normalize_products(df):
  # Load data from the CSV file
  # df = pd.read_csv(file_path)
  
  # Check if the 'price' column has null values
  mask = df['price'].isna()
  
  # If there are null values, assign a random number between 150 and 350 and round to 2 decimals
  df.loc[mask, 'price'] = np.round(np.random.uniform(150, 350, size=mask.sum()), 2)
  
  # Round all prices to 2 decimals
  df['price'] = df['price'].round(2)
  
  # Save the changes to the same file
  df.to_csv(file_path, index=False)

def separate_products_by_options(products_df):
  # Create an empty DataFrame to store the expanded products
  expanded_products = pd.DataFrame()
  
  for index, row in products_df.iterrows():
    # Load the 'options' column as a JSON object
    # options = json.loads(row["options"])

    options_str = row['options'].replace("'", '"')
    try:
      options = json.loads(options_str)
    except json.JSONDecodeError as e:
      print(f"Error decoding JSON for row {index}: {e}")
      continue  # Skip this row or handle differently
    
    # Iterate over each color and storage combination
    for color in options["colors"]:
      for storage in options["storages"]:
        # Create a copy of the current row to modify
        new_row = row.copy()
        
        # Modify the product ID to include the color and storage code
        new_row['id'] = f"{row['id']}-{color['code']}-{storage['code']}"
        
        # Add the modified row to the new DataFrame
        # expanded_products = expanded_products.append(new_row, ignore_index=True)
        expanded_products = pd.concat([expanded_products, pd.DataFrame([new_row])], ignore_index=True)
  
  # print(expanded_products)
  return expanded_products

if __name__ == "__main__":
  file_path = 'data/raw/smartphones/product_details.csv'
  products_df = pd.read_csv(file_path)
  processed_products_df = separate_products_by_options(products_df)
  normalize_products(processed_products_df)
