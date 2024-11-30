# Question Generation from Textbooks

## Overview

This project aims to generate contextually relevant questions from textbooks based on user-provided input. The system leverages embeddings and a fine-tuned question generation model to produce high-quality questions tailored to specific topics or keywords.

## Features

- **Text Chunking**: Text extracted from textbooks is split into manageable chunks.
- **Embeddings Generation**: Each chunk is converted into embeddings using the **Universal Sentence Encoder (USE)**.
- **Efficient Retrieval**: A **Nearest Neighbor** model is fitted on the embeddings to quickly retrieve relevant chunks for any input query.
- **Question Generation**: The retrieved chunks are passed through a **Pegasus model fine-tuned on the SQuAD dataset** to generate relevant questions.

## Workflow

1. **Extract Text**: Input textbook text is extracted and preprocessed.
2. **Chunking**: The text is split into smaller chunks for better embedding generation.
3. **Embedding Creation**: Each chunk is embedded using USE.
4. **Nearest Neighbor Fitting**: A Nearest Neighbor model is trained on the embeddings for fast retrieval.
5. **Input Query**: User provides a keyword or phrase.
6. **Query Embedding**: The input is embedded using USE.
7. **Relevant Chunk Retrieval**: The Nearest Neighbor model retrieves the most relevant text chunks.
8. **Question Generation**: The retrieved chunks are fed into the fine-tuned Pegasus model to generate questions.

## Example

### Input
**Query**: *Photosynthesis*

### Output
1. What is the process of photosynthesis?
2. Which organisms perform photosynthesis?
3. What are the key components involved in photosynthesis?
