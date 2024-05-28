from setuptools import setup, find_packages

setup(
  name='ecommerce-recommender-system',
  version='0.1.0',
  packages=find_packages(),
  install_requires=[
    'pandas',
    'numpy',
    'scikit-learn',
    'fastapi',
    'uvicorn',
    'pytest',
    'pickle'
  ],
)
