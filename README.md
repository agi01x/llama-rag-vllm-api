# RAG API with LLaMA 3.2

This project deploys a private Retrieval-Augmented Generation (RAG) API using LLaMA 3.2 and vLLM.

## Features

✅ Serverless (scale to zero)
✅ Private API
✅ Your own infrastructure
✅ Multi-GPU support

## Installation

1. Clone this repository:
   ```
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure these modules are in your project directory:
   - ingestion.py
   - retriever.py
   - prompt_template.py

## LLaMA Model Setup

1. Download LLaMA model weights from [appropriate source].
2. Place weights in [appropriate directory].
3. Update `model_name` in `rag.py` if necessary.

## Usage

1. Add documents to chat with in the `./docs` folder.

2. Start the server:
   ```
   python server.py
   ```

3. Use the API:
   ```
   python client.py --query "Your question here"
   ```

## Deployment

- Expose the server to the internet (authentication optional)
- Enable "auto start" for serverless operation
- Optimize performance with LitServe features (batching, multi-GPU, etc.)

## Background

This project utilizes:
- RAG (Retrieval-Augmented Generation)
- vLLM for efficient LLM serving
- Vector database (self-hosted Qdrant)
- LitServe for scalable inference

For more details on these components, refer to the full documentation.
