import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from recommender.algorithms.collaborative_filtering import CollaborativeFiltering
import pickle

def main():
  # Load the processed data
  data = pd.read_csv('data/processed/data.csv')
  
  # Train the model
  cf_model = CollaborativeFiltering(data)
  cf_model.train()

  # Ensure the directory to save the model exists
  model_dir = 'data/models'
  os.makedirs(model_dir, exist_ok=True)
  
  # Save the trained model using pickle
  model_path = os.path.join(model_dir, 'model.pkl')
  with open(model_path, 'wb') as model_file:
    pickle.dump(cf_model, model_file)

if __name__ == "__main__":
  main()
