"""
PDF Handler Module
Extracts text and metadata from PDF files
"""

import PyPDF2
import io
from typing import Dict, Any, Tuple


class PDFHandler:
    """Handle PDF file extraction and processing"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes, max_pages: int = None) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_bytes: PDF file content as bytes
            max_pages: Maximum number of pages to extract (None = all pages)
            
        Returns:
            Extracted text from PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            pages_to_read = len(pdf_reader.pages)
            
            if max_pages and max_pages > 0:
                pages_to_read = min(max_pages, pages_to_read)
            
            for page_num in range(pages_to_read):
                page = pdf_reader.pages[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def get_pdf_metadata(pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Get metadata from PDF file
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Dictionary containing PDF metadata
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            metadata = pdf_reader.metadata
            
            return {
                "num_pages": len(pdf_reader.pages),
                "title": metadata.title if metadata else None,
                "author": metadata.author if metadata else None,
                "subject": metadata.subject if metadata else None,
                "creator": metadata.creator if metadata else None,
            }
        
        except Exception as e:
            return {
                "num_pages": 0,
                "error": f"Could not extract metadata: {str(e)}"
            }
    
    @staticmethod
    def summarize_pdf_content(pdf_bytes: bytes, max_chars: int = 2000) -> str:
        """
        Extract and summarize PDF content for context
        
        Args:
            pdf_bytes: PDF file content as bytes
            max_chars: Maximum characters to return
            
        Returns:
            Summarized PDF content
        """
        try:
            text = PDFHandler.extract_text_from_pdf(pdf_bytes, max_pages=5)
            
            # Clean up text
            text = " ".join(text.split())  # Remove extra whitespace
            
            # Return truncated text
            if len(text) > max_chars:
                return text[:max_chars] + "..."
            
            return text
        
        except Exception as e:
            return f"Error summarizing PDF: {str(e)}"
    
    @staticmethod
    def validate_pdf(pdf_bytes: bytes) -> Tuple[bool, str]:
        """
        Validate if bytes represent a valid PDF
        
        Args:
            pdf_bytes: File content as bytes
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            if not pdf_bytes.startswith(b'%PDF'):
                return False, "Not a valid PDF file (missing PDF header)"
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            
            if len(pdf_reader.pages) == 0:
                return False, "PDF has no pages"
            
            return True, "Valid PDF"
        
        except Exception as e:
            return False, f"PDF validation error: {str(e)}"
