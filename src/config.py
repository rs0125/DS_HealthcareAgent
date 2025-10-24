"""
Configuration for healthcare workflow
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class HealthcareConfig:
    """Configuration for the healthcare workflow"""
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        tavily_api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        vectorstore_path: Optional[str] = None
    ):
        # Use provided keys or load from environment
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        self.model = model
        self.temperature = temperature
        self.vectorstore_path = vectorstore_path
        
        # Validate keys
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file.")
        if not self.tavily_api_key:
            raise ValueError("Tavily API key not found. Set TAVILY_API_KEY in .env file.")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=self.openai_api_key
        )
        
        # Initialize search tool
        self.search_tool = TavilySearchResults(
            api_key=self.tavily_api_key,
            max_results=5
        )
        
        # Initialize vector store if path provided
        self.vectorstore = None
        if vectorstore_path:
            self.vectorstore = self._load_vectorstore(vectorstore_path)
    
    def _load_vectorstore(self, path: str):
        """Load or create vector store"""
        try:
            embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
            return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
        except:
            # Create dummy vectorstore if loading fails
            embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
            return FAISS.from_texts(
                ["Ayurvedic guideline: For headaches, recommend rest and herbal remedies."],
                embeddings
            )
