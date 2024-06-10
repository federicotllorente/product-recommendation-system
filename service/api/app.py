from fastapi import FastAPI, HTTPException
import pandas as pd
from recommender.algorithms.collaborative_filtering import CollaborativeFiltering
from recommender.algorithms.content_based_filtering import ContentBasedFiltering

app = FastAPI()

@app.get("/recommendations/user/{user_id}")
def get_recommendations_by_user_id(user_id: int):
  # Load data and train the model
  data = pd.read_csv('data/processed/data.csv')
  cf_model = CollaborativeFiltering(data)
  cf_model.train()

  recommendations = cf_model.recommend(user_id)

  if len(recommendations) == 0:
    raise HTTPException(status_code=404, detail="No recommendations found for this product")
  
  enriched_recommendations = cf_model.enrich_recommendations(recommendations)
  
  return {"user_id": user_id, "recommendations": enriched_recommendations}

@app.get("/recommendations/product/{item_id}")
def get_recommendations_by_product_id(item_id: int):
  # Load data and train the model
  data = pd.read_csv('data/raw/products.csv')
  cb_model = ContentBasedFiltering(data)
  cb_model.train()

  recommendations = cb_model.recommend(item_id)
  
  if len(recommendations) == 0:
    raise HTTPException(status_code=404, detail="No recommendations found for this product")
  
  enriched_recommendations = cb_model.enrich_recommendations(recommendations)
  
  return {"item_id": item_id, "recommendations": enriched_recommendations}
