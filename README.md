
# Anthropic-Hackathon

# Healthcare Document Interrogation System

The Healthcare Document Interrogation System uses the Anthropic Claude 3.5 API to allow users to upload healthcare documents and ask questions to extract relevant information. This system leverages advanced NLP techniques to provide accurate, context-aware responses, enhancing information retrieval in the healthcare sector.

![Healthcare Document Interrogation System Interface](image.png)

## Build with Claude June 2024 Contest

We're excited to announce our participation in the Build with Claude June 2024 contest! This contest invites developers to create innovative projects using Claude through the Anthropic API.

### Contest Details:
- **Duration**: The two-week virtual hackathon runs from June 26th, 2024 at 12pm PT to July 10th, 2024 at 12pm PT.
- **Prizes**: The top three projects will each receive $10,000 worth of Anthropic API credits.

## Leveraging Claude 3.5 Capabilities

We utilize Claude 3.5's advanced capabilities to enhance our system:

- **Contextual Understanding:** Claude 3.5's deep contextual understanding ensures that the responses are highly relevant to the queries.
- **Advanced NLP:** Claude 3.5 employs cutting-edge natural language processing techniques to interpret and respond to complex medical queries accurately.
- **Dynamic Query Processing:** Claude 3.5 dynamically adjusts its responses based on the context and specificity of the questions asked.
- **Multi-turn Conversations:** Support for multi-turn conversations allows for follow-up questions and deeper interaction.
- **Vision Capabilities:** Claude 3.5 includes vision capabilities to analyze and extract information from images within healthcare documents, providing a more comprehensive understanding of the content.

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
- **Image Analysis**: Utilize Claude's vision capabilities to extract information from images in healthcare documents.

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Anthropic--Hackathon.git
   cd Anthropic--Hackathon
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up your Anthropic API key:
   Create a `.env` file in the root directory and add your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   poetry run streamlit run rag/app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload a healthcare-related PDF document using the file uploader in the sidebar.

4. Ask questions about the document in the chat interface.

### Example Queries

- "What are the main symptoms of COVID-19 described in the document?"
- "Can you summarize the treatment options for diabetes mentioned in the text?"
- "Are there any contraindications for the medication discussed on page 3?"

## Configuration

- Model selection: The current implementation uses Claude 3.5 Sonnet. To change the model, modify the `model_name` variable in `rag/app.py`.
- RAG process customization: Adjust the `similarity_top_k` and `node_postprocessors` parameters in the `chat_engine` creation in `rag/app.py`.

## Testing

To run the tests:

```bash
poetry run pytest
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

## Dependencies

Key dependencies include:
- streamlit
- llama-index
- anthropic
- PyPDF2
- PyMuPDF
- sentence-transformers

For a complete list, refer to the `pyproject.toml` file.

## Troubleshooting

- **API Key Issues**: Ensure your Anthropic API key is correctly set in the `.env` file or provided through the Streamlit interface.
- **PDF Processing Errors**: Make sure the uploaded PDF is not corrupted and is readable.
- **Out of Memory Errors**: Large documents may cause memory issues. Try processing smaller documents or increasing your system's RAM.

## Future Improvements

- Implement multi-document querying
- Add support for more file formats (e.g., .docx, .txt)
- Enhance the user interface for better visualization of document structure
- Implement a feedback mechanism for continuous improvement of responses

## Contributors

- Sibomana Glorry
- Kato Steven Mubiru

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Anthropic for providing the Claude 3.5 API
- The LlamaIndex team for their excellent indexing library
- Streamlit for the user-friendly web application framework

## Contact

For any queries or feedback, please open an issue on this GitHub repository or contact the maintainers directly at:
- glorrysibomana758@gmail.com
- kato.steven60@gmail.com

## Disclaimer

This project is a prototype and should not be used for actual medical diagnosis or treatment. Always consult with a qualified healthcare professional for medical advice.
