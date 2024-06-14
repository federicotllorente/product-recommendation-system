from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import pandas as pd
import numpy as np

from recommender.algorithms.collaborative_filtering import CollaborativeFiltering
from recommender.algorithms.content_based_filtering import ContentBasedFiltering

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # TODO
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def float_handler(x):
  if np.isnan(x) or np.isinf(x):
    return None
  return x

# Just for testing purposes - This should be managed by the products service
@app.get("/products")
def get_products(page: int = Query(default=1, ge=1)):
  data = pd.read_csv('data/raw/smartphones/product_details.csv')
  products = data.to_dict(orient='records')
  
  # Pagination
  items_per_page = 20
  start_index = (page - 1) * items_per_page
  end_index = start_index + items_per_page
  paginated_products = products[start_index:end_index]
  total_pages = len(products) // items_per_page + 1

  if page > total_pages:
    raise HTTPException(status_code=400, detail="Invalid page number")

  return {
    "products": jsonable_encoder(paginated_products, custom_encoder={float: float_handler}),
    "count": len(paginated_products),
    "page": page,
    "total_pages": total_pages
  }

# Just for testing purposes - This should be managed by the products service
@app.get("/products/{item_id}")
def get_product_by_id(item_id: str):
  data = pd.read_csv('data/raw/smartphones/product_details.csv')
  
  product = data[data['id'] == item_id].to_dict(orient='records')
  
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  return jsonable_encoder(product[0], custom_encoder={float: float_handler})

@app.get("/recommendations/user/{user_id}")
def get_recommendations_by_user_id(user_id: int):
  # Load data and train the model
  data = pd.read_csv('data/processed/smartphones/data.csv')
  cf_model = CollaborativeFiltering(data)
  cf_model.train()

  recommendations = cf_model.recommend(user_id)

  if len(recommendations) == 0:
    raise HTTPException(status_code=404, detail="No recommendations found for this product")
  
  enriched_recommendations = cf_model.enrich_recommendations(recommendations)
  
  return {
    "user_id": user_id,
    "recommendations": jsonable_encoder(enriched_recommendations, custom_encoder={float: float_handler}),
    "count": len(enriched_recommendations)
  }

@app.get("/recommendations/product/{item_id}")
def get_recommendations_by_product_id(item_id: str):
  # Load data and train the model
  data = pd.read_csv('data/raw/smartphones/product_details.csv')
  cb_model = ContentBasedFiltering(data)
  cb_model.train()

  recommendations = cb_model.recommend(item_id)
  
  if len(recommendations) == 0:
    raise HTTPException(status_code=404, detail="No recommendations found for this product")
  
  enriched_recommendations = cb_model.enrich_recommendations(recommendations)
  
  return {
    "item_id": item_id,
    "recommendations": jsonable_encoder(enriched_recommendations, custom_encoder={float: float_handler}),
    "count": len(enriched_recommendations)
  }

# Just for testing purposes - This should be managed by the products service
@app.post("/cart")
def add_to_cart():
  return { 'count': 1 }
