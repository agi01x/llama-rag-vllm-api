import os
from typing import Iterator, Tuple, Dict, List
from PyPDF2 import PdfReader
from fastembed import TextEmbedding
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, OptimizersConfigDiff, VectorParams


def setup_qdrant_client(url: str, collection_name: str) -> QdrantClient:
    client = QdrantClient(url=url, prefer_grpc=False)
    
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.DOT,
                on_disk=True,
            ),
            optimizers_config=OptimizersConfigDiff(
                default_segment_number=5,
                indexing_threshold=1000,
            )
        )
    return client


class PDFDataLoader:
    def __init__(self, directory: str):
        self.directory = directory
        self.pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    def __iter__(self) -> Iterator[Tuple[str, Dict[str, str]]]:
        for pdf_file in self.pdf_files:
            file_path = os.path.join(self.directory, pdf_file)
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                metadata = {
                    'file_name': pdf_file,
                    'page_number': str(page_num + 1),
                    'text': text
                }
                yield text, metadata


def ingest_data(client: QdrantClient, collection_name: str, embeddings: List[List[float]], batch_metadata: List[Dict[str, str]]) -> None:
    client.upload_collection(
        collection_name=collection_name,
        vectors=embeddings,
        payload=batch_metadata,
    )


def process_pdfs(directory: str, client: QdrantClient, collection_name: str, embedding_model: TextEmbedding, batch_size: int = 32) -> None:
    
    # Create the data loader
    data_loader = PDFDataLoader(directory)
    
    # Process the PDFs in batches
    batch_texts: List[str] = []
    batch_metadata: List[Dict[str, str]] = []
    
    for text, metadata in tqdm(data_loader, desc="Processing PDFs"):
        batch_texts.append(text)
        batch_metadata.append(metadata)
        
        if len(batch_texts) == batch_size:
            # Generate embeddings for the batch
            embeddings = embedding_model.embed(batch_texts)
            
            try:
                ingest_data(client, collection_name, embeddings, batch_metadata)
            except Exception as e:
                print(f"Error ingesting data: {e}")
            
            # Clear the batch
            batch_texts = []
            batch_metadata = []
    
    # Process any remaining items
    if batch_texts:
        embeddings = embedding_model.embed(batch_texts)
        ingest_data(client, collection_name, embeddings, batch_metadata)


def ingest_pdfs(pdf_directory: str, embedding_model: TextEmbedding, qdrant_url: str = "http://localhost:6333", collection_name: str = "qdrant_collection") -> None:
    client = setup_qdrant_client(qdrant_url, collection_name)
    process_pdfs(pdf_directory, client, collection_name, embedding_model)