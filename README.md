# Project Setup

## Installation

1. Clone this repository:
   ```
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure the following local modules are present in your project directory:
   - ingestion.py
   - retriever.py
   - prompt_template.py

## LLaMA Model Setup

This project uses the LLaMA model. To set it up:

1. Download the LLaMA model weights from [insert appropriate source].
2. Place the model weights in [insert appropriate directory].
3. Update the `model_name` variable in `rag.py` if necessary.

## Running the Application

To run the application:
