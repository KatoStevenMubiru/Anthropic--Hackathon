# Anthropic-Hackathon

# Healthcare Document Interrogation System

The Healthcare Document Interrogation System uses the Anthropic Claude 3.5 API to allow users to upload healthcare documents and ask questions to extract relevant information. This system leverages advanced NLP techniques to provide accurate, context-aware responses, enhancing information retrieval in the healthcare sector.

## Build with Claude June 2024 Contest

We're excited to announce our participation in the Build with Claude June 2024 contest! This contest invites developers to create innovative projects using Claude through the Anthropic API.

### Contest Details:
- **Duration**: The two-week virtual hackathon runs from June 26th, 2024 at 12pm PT to July 10th, 2024 at 12pm PT.
- **Prizes**: The top three projects will each receive $10,000 worth of Anthropic API credits.

## Project Overview

This project demonstrates the use of the following components:

### Indexing with Llama Index
We use the Llama Index to create a vector store from healthcare documents, enabling efficient and accurate information retrieval.

### Using Your Anthropic API Credits
Participants can use their Anthropic API credits to test and refine their projects, ensuring the highest quality and performance.

## Features

- **Upload Healthcare Documents**: Easily upload and process healthcare-related PDFs.
- **Chat with Claude**: Ask questions and get context-aware responses from the documents.
- **Query Categorization**: Automatically categorize queries to provide more relevant answers.
- **Response Formatting**: Format responses based on the category of the query for better understanding.

## Installation

To install the required dependencies, use the following command:

```bash
poetry install
```

## Running the Application

To run the application, use the following command:

```bash
streamlit run rag/app.py
```

## Directory Structure

```
Anthropic--Hackathon/
├── rag/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── app.py
│   ├── claude_llm.py
│   ├── document_processor.py
│   ├── healthcare_utils.py
├── tests/
│   ├── __init__.py
│   └── test_healthcare_rag.py
├── venv/
├── .env
├── .gitattributes
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Contribution

This project is not open to public contributions. However, we welcome feedback and suggestions. Feel free to reach out via GitHub.

## Contributors

- Sibomana Glorry
- Kato Steven Mubiru

## License

This project is licensed under the MIT License.

