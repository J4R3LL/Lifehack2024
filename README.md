# Creating LLM Model By Scraping Website Content

## Introduction

This project aims to generate a knowledge graph using artificial intelligence. The process involves extracting information from articles and using a pre-trained model to build relationships between entities. Two main components are involved: `articles.py` and `model.py`.

## Installation

Before running the project, ensure you have the required packages installed:

```bash
pip install networkx transformers huggingface_hub requests bs4 Torch==2.2.2 spacy
python -m spacy download en_core_web_sm
```

## Usage
Running `model.py` will run the LLM and prompt you for you question/input. The model will generate text to answer your question

### articles.py

The `articles.py` script is responsible for loading the necessary articles needed to create the knowledge graph. It extracts relevant information from these articles and prepares the data for the knowledge graph generation process.

```bash
python articles.py
```

### model.py

The `model.py` script contains the model implementation and handles the AI aspect of the project. It imports the necessary model and runs the AI to generate relationships between entities based on the provided prompt.

```bash
python model.py
```

