import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import pickle
from recommender.algorithms.collaborative_filtering import CollaborativeFiltering
from recommender.algorithms.content_based_filtering import ContentBasedFiltering
from recommender.algorithms.content_and_price_based_filtering import ContentAndPriceBasedFiltering

def train_collaborative_filtering():
  print('Training collaborative filtering algorithm')

  # Load the processed data
  data = pd.read_csv('data/processed/data.csv')
  
  # Train the model
  cf_model = CollaborativeFiltering(data)
  cf_model.train()

  # Ensure the directory to save the model exists
  model_dir = 'data/models'
  os.makedirs(model_dir, exist_ok=True)
  
  # Save the trained model using pickle
  model_path = os.path.join(model_dir, 'collaborative_filtering.pkl')
  with open(model_path, 'wb') as model_file:
    pickle.dump(cf_model, model_file)

def train_content_based_filtering():
  print('Training content-based algorithm')

  # Load the processed data
  data = pd.read_csv('data/raw/products.csv')
  
  # Train the model
  cb_model = ContentBasedFiltering(data)
  cb_model.train()

  # Ensure the directory to save the model exists
  model_dir = 'data/models'
  os.makedirs(model_dir, exist_ok=True)
  
  # Save the trained model using pickle
  model_path = os.path.join(model_dir, 'content_based_filtering.pkl')
  with open(model_path, 'wb') as model_file:
    pickle.dump(cb_model, model_file)

def train_content_and_price_based_filtering():
  print('Training content-and-price-based algorithm')

  # Load the processed data
  data = pd.read_csv('data/raw/products.csv')
  
  # Train the model
  cpb_model = ContentAndPriceBasedFiltering(data)
  cpb_model.train()

  # Ensure the directory to save the model exists
  model_dir = 'data/models'
  os.makedirs(model_dir, exist_ok=True)
  
  # Save the trained model using pickle
  model_path = os.path.join(model_dir, 'content_and_price_based_filtering.pkl')
  with open(model_path, 'wb') as model_file:
    pickle.dump(cpb_model, model_file)

def train_all():
  print('Training all algorithms')
  train_collaborative_filtering()
  train_content_based_filtering()
  train_content_and_price_based_filtering()

if __name__ == "__main__":
  if '-cf' in sys.argv:
    train_collaborative_filtering()
  elif '-cb' in sys.argv:
    train_content_based_filtering()
  elif '-cpb' in sys.argv:
    train_content_and_price_based_filtering()
  else:
    train_all()
