**Note:** you should execute all the mentioned commands here from the project root

## Install dependencies

```
pip install --no-cache-dir -r requirements.txt
```

## Generate raw data if empty

Products:

```
python data/scripts/generate_products.py
```

Ratings:

```
python data/scripts/generate_ratings.py
```

## Preprocess the generated data

```
python data/scripts/preprocess.py
```

## Train the model (and save it)

```
python recommender/train.py
```

The model will be saved in a `.pkl` file in `/data/models/`
