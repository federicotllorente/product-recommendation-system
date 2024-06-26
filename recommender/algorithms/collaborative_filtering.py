import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
  def __init__(self, data):
    self.data = data
    self.user_item_matrix = self.create_user_item_matrix()
    self.user_similarity = None

  def create_user_item_matrix(self):
    user_item_matrix = self.data.pivot(index='user_id', columns='item_id', values='rating')
    user_item_matrix.fillna(0, inplace=True)
    return user_item_matrix

  def train(self):
    # Calculate cosine similarity between users
    self.user_similarity = cosine_similarity(self.user_item_matrix)
    # print("User similarity matrix:")
    # print(self.user_similarity)

  def recommend(self, user_id, num_recommendations=10):
    if self.user_similarity is None:
      raise Exception("Model has not been trained yet")

    # Find the user index in the matrix
    user_index = self.user_item_matrix.index.get_loc(user_id)
    
    # Get user ratings
    user_ratings = self.user_item_matrix.iloc[user_index].values
    
    # Calculate the recommendation score for each product
    scores = self.user_similarity[user_index].dot(self.user_item_matrix) / np.array([np.abs(self.user_similarity[user_index]).sum()])
    
    # Do not recommend products that the user has already rated
    scores[user_ratings > 0] = -1
    
    # Get the indices of the products with the highest scores
    recommended_indices = np.argsort(scores)[::-1][:num_recommendations]
    
    # Get the IDs of the recommended products
    recommended_item_ids = self.user_item_matrix.columns[recommended_indices]
    
    return recommended_item_ids.tolist()
  
  def enrich_recommendations(self, recommended_product_ids):
    # Filter the data to get the details of the recommended products
    enriched_recommendations = self.data[self.data['item_id'].isin(recommended_product_ids)]

    # Drop duplicates by 'item_id'
    enriched_recommendations = enriched_recommendations.drop_duplicates(subset='item_id')

    # Reorder the recommendations to match the order of recommended_product_ids
    enriched_recommendations = enriched_recommendations.set_index('item_id').reindex(recommended_product_ids).reset_index()

    # Drop unnecessary columns
    enriched_recommendations = enriched_recommendations.drop(columns=['rating'])
    enriched_recommendations = enriched_recommendations.drop(columns=['user_id'])

    # Rename column 'item_id' to 'id'
    enriched_recommendations.rename(columns={'item_id': 'id'}, inplace=True)

    return enriched_recommendations.to_dict(orient='records')

if __name__ == "__main__":
  # Load data
  data = pd.read_csv("data/processed/data.csv", usecols=['user_id', 'item_id', 'rating', 'name', 'category', 'price', 'description'])

  # Train the model
  cf = CollaborativeFiltering(data)
  cf.train()

  # Get recommendations for a specific user
  user_id = 200
  recommendations = cf.recommend(user_id)

  # Enrich recommendations with product details
  enriched_recommendations = cf.enrich_recommendations(recommendations)

  print(f"Recommendations for user {user_id}", enriched_recommendations)
