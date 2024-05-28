import csv
import random

def generate_products(num_items, price_range=(10.0, 2500.0), categories=[], file_path='data/raw/products.csv'):
  """
  Generates product data and writes it to a CSV file

  Args:
  num_items (int): Number of products to generate
  price_range (tuple): A tuple containing the minimum and maximum price
  categories (list): A list of categories to assign to products
  """
  with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'category', 'price'])
    
    for item_id in range(1, num_items + 1):
      category = random.choice(categories)
      name = f"{category} {item_id}"
      price = random.uniform(*price_range)
      writer.writerow([item_id, name, category, round(price, 2)])

if __name__ == "__main__":
  num_items = 5000
  price_range = (10.0, 120.0)
  categories = [
    'Kitchen Knives', 'Cutting Boards', 'Frying Pans', 'Pots', 'Kitchen Utensils',
    'Mixing Bowls', 'Measuring Cups', 'Measuring Spoons', 'Graters', 'Peelers',
    'Colanders', 'Salad Spinners', 'Food Storage Containers', 'Spice Racks', 'Dish Racks',
    'Paper Towel Holders', 'Trivets', 'Oven Mitts', 'Aprons', 'Cooking Thermometers',
    'Timers', 'Blenders', 'Food Processors', 'Microwaves', 'Toasters',
    'Coffee Makers', 'Espresso Machines', 'Kettles', 'Juicers', 'Bread Machines',
    'Waffle Makers', 'Sandwich Makers', 'Rice Cookers', 'Slow Cookers', 'Pressure Cookers',
    'Deep Fryers', 'Grills', 'Skillets', 'Bakeware Sets', 'Cake Pans',
    'Muffin Pans', 'Pizza Stones', 'Cookie Sheets', 'Mixing Paddles', 'Rolling Pins',
    'Pastry Brushes', 'Spatulas', 'Whisks', 'Ladles', 'Tongs'
  ]
  
  generate_products(num_items, price_range, categories)
