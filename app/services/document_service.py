"""
Document processing service for handling file uploads.
Supports PDF and text file formats.
"""
from pypdf import PdfReader
from typing import List
import io


class DocumentProcessor:
    """Service for processing uploaded documents."""
    
    def process_pdf(self, file_content: bytes) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Extracted text from the PDF
        """
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    def process_text(self, file_content: bytes) -> str:
        """
        Process text file.
        
        Args:
            file_content: Text file content as bytes
            
        Returns:
            Decoded text content
        """
        return file_content.decode('utf-8')
    
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if chunk_overlap >= chunk_size:
            # Invalid configuration, use no overlap
            chunk_overlap = 0
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position
            end = min(start + chunk_size, text_length)
            
            # Extract chunk
            chunk = text[start:end]
            
            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk)
            
            # If we've reached the end, break
            if end >= text_length:
                break
            
            # Move start position (with overlap)
            start = end - chunk_overlap
        
        return chunks


# Global document processor instance
document_processor = DocumentProcessor()
