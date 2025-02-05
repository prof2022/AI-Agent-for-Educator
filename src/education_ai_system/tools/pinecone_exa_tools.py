# src/education_ai_system/tools/pinecone_exa_tools.py

import os
import json
import torch
from transformers import AutoTokenizer, AutoModel
from pydantic import Field
from typing import List, Optional
from dotenv import load_dotenv
from crewai_tools import BaseTool
from exa_py import Exa
import pinecone
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Initialize Pinecone and embedding model
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME", "seismic-agent")

if not api_key:
    print("Error: Pinecone API key is missing. Check your environment variables.")
    raise ValueError("Missing Pinecone API key.")

# Initialize the Pinecone client using the recommended approach
pc = Pinecone(api_key=api_key)
print("Pinecone client initialized.")

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

class PineconeRetrievalTool(BaseTool):
    """Tool to retrieve relevant context from Pinecone vector database based on user query."""
    index: Optional[pinecone.Index] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like Pinecone Index

    def __init__(self):
        # Initialize BaseTool with name and description
        name = "Pinecone Retrieval Tool"
        description = (
            "Fetches context from the Pinecone vector database based on a user query. "
            "It retrieves relevant text chunks and metadata that align with the query."
        )
        super().__init__(name=name, description=description)

        # Check if index exists; if not, create it
        try:
            available_indexes = pc.list_indexes().names()
            if index_name not in available_indexes:
                print(f"Index '{index_name}' does not exist. Creating it now...")
                # Define index creation specifications
                spec = ServerlessSpec(
                    cloud='aws',      # Adjust as needed
                    region='us-west-2' # Adjust as needed
                )
                pc.create_index(
                    name=index_name,
                    dimension=384,
                    metric='cosine',
                    spec=spec
                )
                print(f"Index '{index_name}' created successfully.")
            else:
                print(f"Index '{index_name}' found.")

            # Connect to the Pinecone index
            self.index = pc.Index(index_name)
            print(f"Successfully connected to Pinecone index: {index_name}")
        except Exception as e:
            print(f"Error initializing Pinecone index '{index_name}': {e}")
            self.index = None

    def _run(self, query: str, num_results: int = 1) -> str:
        # Check if index is initialized
        if not self.index:
            return "Pinecone index is not initialized."

        # Generate embedding for the query
        query_vector = self._get_query_embedding(query)
        print(f"Generated query embedding: {query_vector[:5]}...")  # Show a sample of the embedding

        try:
            # Attempt to retrieve from Pinecone
            response = self.index.query(vector=query_vector, top_k=num_results, include_metadata=True)
            if "matches" not in response:
                print("Warning: No matches found in Pinecone query response.")

            # Process results to return JSON-serializable output
            results = [
                {
                    "score": match.get("score", 0),
                    "metadata": match.get("metadata", {})
                }
                for match in response.get("matches", [])
            ]
            return json.dumps(results, indent=2)
        except Exception as e:
            print(f"Error during Pinecone query: {e}")
            return f"Error querying Pinecone index: {e}"

    def _get_query_embedding(self, text: str) -> List[float]:
        # Generate embedding for the query
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            query_embedding = model(**inputs).last_hidden_state.mean(dim=1).cpu().numpy().squeeze()
        
        return query_embedding.tolist()

class ExaSearchContextualTool(BaseTool):
    """Tool to perform an Exa web search using contextual information from Pinecone retrieval."""

    def __init__(self):
        # Initialize BaseTool with name and description
        name = "ExaSearchContextualTool"
        description = (
            "Uses the Exa API to perform a web search based on contextual information from Pinecone. "
            "Finds the most recent and relevant online materials aligned with the given context."
        )
        super().__init__(name=name, description=description)

    def _run(self, search_query: str) -> str:
        # Initialize the Exa API client with the provided key
        exa = Exa(os.getenv("EXASEARCH_API_KEY"))

        # Execute a search using the Exa API
        search_response = exa.search_and_contents(
            search_query,
            use_autoprompt=True,
            text={"include_html_tags": False, "max_characters": 8000},
        )
        
        # Process search results and safely access attributes
        try:
            # Assuming `results` is a list attribute in `search_response`
            results = [
                {
                    "title": getattr(result, "title", "No title available"),
                    "link": getattr(result, "url", "No URL available"),
                    "snippet": getattr(result, "snippet", "No snippet available"),
                }
                for result in getattr(search_response, "results", [])
            ]
        except AttributeError as e:
            return f"Error processing results: {e}"

        # Return the results as a JSON string for consistency
        return json.dumps(results, indent=2)
