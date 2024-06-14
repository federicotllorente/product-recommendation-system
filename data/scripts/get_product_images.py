import pandas as pd
import os
import requests

def fetch_and_save_images(csv_path):
  # Read the CSV file containing the list of products
  df = pd.read_csv(csv_path)
  
  # Create the directory if it does not exist
  images_directory = 'data/raw/smartphones/images'
  if not os.path.exists(images_directory):
    os.makedirs(images_directory)
  
  # Add a new column for the internal image URL
  df['internalImgUrl'] = None
  
  # Iterate over each row of the DataFrame
  for index, row in df.iterrows():
    image_url = row['imgUrl']
    product_id = row['id']

    print(f"Processing image: {image_url}")
    
    # Check if the image URL is not empty
    if pd.notna(image_url):
      try:
        # Get the image from the URL
        response = requests.get(image_url)
        if response.status_code == 200:
          # Save the image in the specified directory
          image_path = os.path.join(images_directory, f"{product_id}.jpg")
          with open(image_path, 'wb') as file:
            file.write(response.content)
          
          # Save the image path in the DataFrame
          df.at[index, 'internalImgUrl'] = image_path
          
          print(f"Saved image: {image_path}")
        else:
          print(f"Image download failed: {image_url}")
      except Exception as e:
        print(f"Image processing failed: {product_id}: {e}")

  # Save the updated DataFrame in the same CSV file
  df.to_csv(csv_path, index=False)

if __name__ == "__main__":
  csv_path = 'data/raw/smartphones/product_details.csv'
  fetch_and_save_images(csv_path)
