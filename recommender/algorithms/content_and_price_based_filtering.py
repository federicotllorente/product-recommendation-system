import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class ContentAndPriceBasedFiltering:
  def __init__(self, data):
    self.data = data
    self.product_features = None
    self.product_similarity = None

  def _extract_features(self):
    # Combine relevant product features into a single string
    self.data['combined_features'] = self.data['name'] + ' ' + self.data['category'] + ' ' + self.data['description']
    
    # Initialize TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the text data
    tfidf_features = tfidf_vectorizer.fit_transform(self.data['combined_features'])

    # Normalize prices
    scaler = MinMaxScaler()
    normalized_prices = scaler.fit_transform(self.data[['price']])
    
    # Combine TF-IDF features with normalized price
    self.product_features = np.hstack((tfidf_features.toarray(), normalized_prices))

  def train(self):
    # Extract features from the data
    self._extract_features()

    # Calculate cosine similarity between product features
    self.product_similarity = cosine_similarity(self.product_features)

  def recommend(self, item_id, num_recommendations=10):
    # Find index of the product in the data
    indices = self.data.index[self.data['id'] == item_id].tolist()
    if not indices:
      return []
    product_index = indices[0]

    # Calculate similarity scores for the given product
    scores = list(enumerate(self.product_similarity[product_index]))

    # Sort the products based on similarity scores
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Exclude the given product itself from recommendations
    sorted_scores = [x for x in sorted_scores if x[0] != product_index]

    # Get top N most similar products
    recommended_indices = [x[0] for x in sorted_scores[:num_recommendations]]

    # Get the IDs of recommended products
    recommended_item_ids = self.data.iloc[recommended_indices]['id']

    return recommended_item_ids.tolist()
  
  def enrich_recommendations(self, recommended_product_ids):
    # Filter the data to get the details of the recommended products
    enriched_recommendations = self.data[self.data['id'].isin(recommended_product_ids)]

    # Drop 'combined_features' column
    enriched_recommendations = enriched_recommendations.drop(columns=['combined_features'])
    
    return enriched_recommendations.to_dict(orient='records')

if __name__ == "__main__":
  # Load example data
  data = pd.read_csv("data/raw/products.csv", usecols=['id', 'name', 'category', 'price', 'description'])

  # Train the model
  cpb_model = ContentAndPriceBasedFiltering(data)
  cpb_model.train()

  # Get recommendations for a given product
  item_id = 1
  recommendations = cpb_model.recommend(item_id)

  # Enrich recommendations with product details
  enriched_recommendations = cpb_model.enrich_recommendations(recommendations)

  print(f"Recommendations for product {item_id}:", enriched_recommendations)
