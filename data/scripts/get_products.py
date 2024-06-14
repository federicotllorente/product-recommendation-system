import requests
import pandas as pd
import os

def fetch_data_and_save():
  # Call the endpoint to get the list of products
  print('Fetching the product list...')
  response = requests.get("https://itx-frontend-test.onrender.com/api/product/")
  
  if response.status_code == 200:
    print('Success fetching the product list')
    products = response.json()
    # Save the list of products to a CSV file
    products_df = pd.DataFrame(products)

    directory = 'data/raw/smartphones'
    
    if not os.path.exists(directory):
      os.makedirs(directory)
    
    products_df.to_csv(f'{directory}/product_list.csv', index=False)
    print('Saved product list into CSV')
    
    # Prepare DataFrame to store product details
    product_details_list = []
    
    # Iterate over the list of products and get details of each one
    for product in products:
      product_id = product['id']
      print(f"Fetching the product details for ID {product_id}...")
      detail_response = requests.get(f"https://itx-frontend-test.onrender.com/api/product/{product_id}")
      if detail_response.status_code == 200:
        print(f"Success fetching the product details for ID {product_id}")
        product_details = detail_response.json()
        product_details_list.append(product_details)
      else:
        print(f"Failed fetching the product details for ID {product_id}")
    
    # Save the product details to another CSV file
    product_details_df = pd.DataFrame(product_details_list)
    product_details_df.to_csv('data/raw/smartphones/product_details.csv', index=False)
    print('Saved product details into CSV')
  else:
    print('Failed fetching the product list')

if __name__ == "__main__":
  # Call the function to execute the process
  fetch_data_and_save()
