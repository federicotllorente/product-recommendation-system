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
python recommender/train.py [-cf|-cb|-cpb]
```

You need to pass an argument as the algorithm to use:

- For **collaborative filtering**: `-cf`

- For **content based filtering**: `-cb`

- For **content and price based filtering**: `-cpb`

The model will be saved in a `.pkl` file in `/data/models/`

## Run the API server

```
uvicorn service.api.app:app --reload
```

This will start running the FastAPI server on [http://127.0.0.1:8000](http://127.0.0.1:8000)
