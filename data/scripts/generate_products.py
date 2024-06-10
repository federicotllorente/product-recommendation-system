import csv
import random

def generate_products(num_items, price_range=(10.0, 2500.0), categories=[], description_adjectives=[], file_path='data/raw/products.csv'):
  """
  Generates product data and writes it to a CSV file

  Args:
  num_items (int): Number of products to generate
  price_range (tuple): A tuple containing the minimum and maximum price
  categories (list): A list of categories to assign to products
  description_adjectives (list): A list of adjectives to assign to product descriptions
  """
  with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'category', 'price', 'description'])
    
    for item_id in range(1, num_items + 1):
      category = random.choice(categories)
      description = f"{random.choice(description_adjectives).capitalize()} {category.lower()}"
      name = f"{category} {item_id}"
      price = random.uniform(*price_range)
      writer.writerow([item_id, name, category, round(price, 2), description])

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

  description_adjectives = [
    "sharp", "durable", "ergonomic", "compact", "versatile",
    "heavy-duty", "lightweight", "sleek", "non-stick", "washable",
    "foldable", "adjustable", "portable", "efficient", "reliable",
    "affordable", "premium", "eco-friendly", "stylish", "modern",
    "traditional", "innovative", "convenient", "robust", "sophisticated",
    "polished", "professional", "multifunctional", "handy", "decorative",
    "powerful", "automatic", "manual", "thermal", "insulated",
    "stainless", "precise", "hygienic", "safe", "sturdy",
    "customizable", "colorful", "classic", "disposable", "reusable",
    "programmable", "digital", "analog", "ceramic", "rustic"
  ]
  
  generate_products(num_items, price_range, categories, description_adjectives)
