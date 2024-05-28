from fastapi import FastAPI
from recommender.algorithms.collaborative_filtering import CollaborativeFiltering
import pandas as pd

app = FastAPI()

# Load data and train the model
data = pd.read_csv('data/processed/data.csv')
cf_model = CollaborativeFiltering(data)
cf_model.train()

@app.get("/recommendations/user/{user_id}")
def get_recommendations(user_id: int):
  recommendations = cf_model.recommend(user_id)
  return {"user_id": user_id, "recommendations": recommendations}
