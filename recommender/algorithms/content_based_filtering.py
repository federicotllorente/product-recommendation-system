import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedFiltering:
  def __init__(self, data):
    self.data = data
    self.product_features = None
    self.product_similarity = None

  def _combine_features(self, columns):
    return self.data.apply(lambda x: ' '.join([str(x[col]) for col in columns]) if not self.data[
        (self.data[columns[0]] == x[columns[0]]) & 
        (self.data[columns[1]] == x[columns[1]]) & 
        (self.data.index != x.name)
        # ~((self.data[columns[0]] == x[columns[0]]) & (self.data[columns[1]] == x[columns[1]]))
    ].empty else '', axis=1)

  def _extract_features(self):
    self.data['combined_features'] = self._combine_features([
      'brand',
      'model',
      'networkTechnology',
      'networkSpeed',
      'displayType',
      'displayResolution',
      'cpu',
      'chipset',
      'gpu',
      'battery'
    ])
    
    # Initialize TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the text data
    self.product_features = tfidf_vectorizer.fit_transform(self.data['combined_features'])

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
    # sorted_scores = [x for x in sorted_scores if x[0] != product_index]

    # Exclude the given product itself and products with the same brand and model from recommendations
    sorted_scores = [x for x in sorted_scores if x[0] != product_index and (self.data.loc[x[0], 'brand'] != self.data.loc[product_index, 'brand'] or self.data.loc[x[0], 'model'] != self.data.loc[product_index, 'model'])]

    # Exclude recommendations with the same model (duplicates, same products but with different options)
    seen_models = set()
    sorted_scores_filtered = []
    for x in sorted_scores:
        if x[0] != product_index:
            model = self.data.loc[x[0], 'model']
            if model not in seen_models:
                sorted_scores_filtered.append(x)
                seen_models.add(model)
    # sorted_scores = sorted_scores_filtered

    # Get top N most similar products
    # recommended_indices = [x[0] for x in sorted_scores[:num_recommendations]]
    recommended_indices = [x[0] for x in sorted_scores_filtered[:num_recommendations]]

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
  data = pd.read_csv("data/raw/smartphones/product_details.csv")

  # Train the model
  cb_model = ContentBasedFiltering(data)
  cb_model.train()

  # Get recommendations for a given product
  item_id = 1
  recommendations = cb_model.recommend(item_id)

  # Enrich recommendations with product details
  enriched_recommendations = cb_model.enrich_recommendations(recommendations)

  print(f"Recommendations for product {item_id}:", enriched_recommendations)
