"""
PDF Selector Component
Displays loaded PDF documents and allows selection for analysis
"""

import streamlit as st
from services import AnalyzerService


def render_pdf_selector(service: AnalyzerService):
    """
    Render PDF selector and info panel
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("📄 PDF Documents")
    
    pdf_names = service.get_pdf_names()
    
    if not pdf_names:
        st.info("👈 Upload a PDF from the sidebar to start analyzing documents")
        return
    
    # Create columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # PDF selector dropdown
        selected_pdf = st.selectbox(
            "Select a PDF to analyze",
            pdf_names,
            index=0 if service.get_current_pdf() not in pdf_names else pdf_names.index(service.get_current_pdf()),
            key="pdf_selector"
        )
        
        if selected_pdf:
            service.set_current_pdf(selected_pdf)
            
            # Get PDF metadata
            metadata = service.get_pdf_metadata(selected_pdf)
            
            # Display PDF info
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Pages", metadata.get("num_pages", 0))
            
            with col_b:
                title = metadata.get("title")
                st.metric("Title", "N/A" if not title else (title[:15] + "..." if len(title) > 15 else title))
            
            with col_c:
                author = metadata.get("author")
                st.metric("Author", "N/A" if not author else (author[:15] + "..." if len(author) > 15 else author))
            
            # PDF content preview
            with st.expander("📖 PDF Preview (First 500 characters)"):
                pdf_text = service.get_pdf_text(selected_pdf)
                if pdf_text:
                    st.text_area(
                        "Content Preview",
                        pdf_text[:500],
                        height=200,
                        disabled=True,
                        key="pdf_preview"
                    )
    
    with col2:
        if st.button("🗑️ Clear All PDFs", key="clear_pdfs_btn"):
            service.clear_pdfs()
            st.success("✅ All PDFs cleared!")
            st.rerun()


def get_pdf_info_badge(service: AnalyzerService) -> str:
    """
    Get a formatted badge showing number of loaded PDFs
    
    Args:
        service: AnalyzerService instance
        
    Returns:
        Formatted string for display
    """
    pdf_count = len(service.get_pdf_names())
    
    if pdf_count == 0:
        return "📄 0 PDFs"
    elif pdf_count == 1:
        return f"📄 1 PDF"
    else:
        return f"📄 {pdf_count} PDFs"
