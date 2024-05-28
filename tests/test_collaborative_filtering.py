import pytest
import pandas as pd
from recommender.algorithms.collaborative_filtering import CollaborativeFiltering

def test_user_item_matrix_creation():
  data = pd.DataFrame({
    'user_id': [1, 1, 2, 2],
    'item_id': [1, 2, 1, 2],
    'rating': [5, 3, 4, 1]
  })
  cf = CollaborativeFiltering(data)
  user_item_matrix = cf.create_user_item_matrix()
  assert user_item_matrix.shape == (2, 2)
