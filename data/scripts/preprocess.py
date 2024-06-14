import pandas as pd
import os

def load_data(ratings_path, products_path):
  ratings_df = pd.read_csv(ratings_path)
  products_df = pd.read_csv(products_path)
  return ratings_df, products_df

def preprocess_data(ratings_df, products_df):
  # Check for null values
  # ratings_df.dropna(inplace=True)
  # products_df.dropna(inplace=True)

  # Rename the 'id' column to 'item_id' in products_df to unify column names
  products_df.rename(columns={'id': 'item_id'}, inplace=True)
  
  # Merge the two tables on the 'item_id' column
  merged_df = pd.merge(ratings_df, products_df, on='item_id')
  
  return merged_df

if __name__ == "__main__":
  ratings_path = "data/raw/smartphones/ratings.csv"
  products_path = "data/raw/smartphones/product_details.csv"
  
  processed_data_directory = "data/processed/smartphones"
  processed_data_path = f"{processed_data_directory}/data.csv"
  
  ratings_df, products_df = load_data(ratings_path, products_path)
  processed_data = preprocess_data(ratings_df, products_df)

  if not os.path.exists(processed_data_directory):
    os.makedirs(processed_data_directory)

  processed_data.to_csv(processed_data_path, index=False)
