import pandas as pd
import numpy as np

def generate_ratings(num_users, num_items, max_ratings_per_user, rating_range=(1, 5), file_path='data/raw/ratings.csv', productList=None):
  """
  Generates a CSV file with user_id, item_id and rating
  
  Args:
  num_users (int): Number of users to generate
  num_items (int): Total number of available items
  max_ratings_per_user (int): Maximum number of ratings a user can generate
  rating_range (tuple): Range of possible rating scores (min and max)
  file_path (str): Path where the CSV file will be stored
  """
  # Determine the random number of ratings per user
  ratings_per_user = np.random.randint(1, max_ratings_per_user + 1, num_users)
  
  # Create the data ensuring there are no duplicates
  all_ratings = []
  for user_id in range(1, num_users + 1):
    items_rated = set()
    for _ in range(ratings_per_user[user_id - 1]):
      item_idx = np.random.randint(1, num_items + 1)
      item_id = item_idx

      if productList and len(productList) >= item_idx:
        item_id = productList[item_idx - 1]

      # Prevent duplicate reviews for a same user
      while item_id in items_rated:
        item_idx = np.random.randint(1, num_items + 1)
        item_id = item_idx

        if productList and len(productList) >= item_idx:
          item_id = productList[item_idx - 1]

      items_rated.add(item_id)
      rating = np.random.randint(rating_range[0], rating_range[1] + 1)
      all_ratings.append((user_id, item_id, rating))
  
  # Convert to a DataFrame
  df = pd.DataFrame(all_ratings, columns=['user_id', 'item_id', 'rating'])
  
  # Save in CSV
  df.to_csv(file_path, index=False)
  print(f'Generated file in: {file_path}')

if __name__ == "__main__":
  num_users = 50 # All these users will 'write' a review
  num_items = 209 # 100
  max_ratings_per_user = 4
  rating_range=(1, 5)
  file_path='data/raw/smartphones/ratings.csv'

  product_details_df = pd.read_csv('data/raw/smartphones/product_details.csv')
  productList = product_details_df['id'].tolist()
  
  generate_ratings(num_users, num_items, max_ratings_per_user, rating_range, file_path, productList)
