import PyPDF2
from fpdf import FPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def create_enhanced_resume(analysis, output_path):
    """Create an enhanced resume PDF with analysis and suggestions."""
    # Create a new FPDF instance with Unicode support
    pdf = FPDF()
    pdf.add_page()
    
    # Set font that supports Unicode characters
    pdf.add_font('DejaVu', '', os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                           '..', 'static', 'fonts', 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.set_font("DejaVu", style="", size=16)
    
    pdf.cell(0, 10, "Enhanced Resume Analysis", ln=True, align="C")
    pdf.ln(10)
    
    # Add personal information
    pdf.set_font("DejaVu", style="", size=14)
    pdf.cell(0, 10, "Personal Information", ln=True)
    pdf.set_font("DejaVu", style="", size=12)
    
    if "personal_info" in analysis:
        for key, value in analysis["personal_info"].items():
            pdf.cell(0, 8, f"{key.capitalize()}: {value}", ln=True)
    
    # Add skills section
    pdf.ln(5)
    pdf.set_font("DejaVu", style="", size=14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("DejaVu", style="", size=12)
    
    if "skills" in analysis and analysis["skills"]:
        for skill in analysis["skills"]:
            pdf.cell(0, 8, f"- {skill}", ln=True)  # Use hyphen instead of bullet
    
    # Add education section
    pdf.ln(5)
    pdf.set_font("DejaVu", style="", size=14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("DejaVu", style="", size=12)
    
    if "education" in analysis and analysis["education"]:
        for edu in analysis["education"]:
            if isinstance(edu, dict):
                for key, value in edu.items():
                    pdf.cell(0, 8, f"{key}: {value}", ln=True)
                pdf.ln(5)
            else:
                pdf.cell(0, 8, f"- {edu}", ln=True)  # Use hyphen instead of bullet
    
    # Add experience section
    pdf.ln(5)
    pdf.set_font("DejaVu", style="", size=14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("DejaVu", style="", size=12)
    
    if "experience" in analysis and analysis["experience"]:
        for exp in analysis["experience"]:
            if isinstance(exp, dict):
                for key, value in exp.items():
                    pdf.cell(0, 8, f"{key}: {value}", ln=True)
                pdf.ln(5)
            else:
                pdf.cell(0, 8, f"- {exp}", ln=True)  # Use hyphen instead of bullet
    
    # Add suggestions
    pdf.add_page()
    pdf.set_font("DejaVu", style="", size=14)
    pdf.cell(0, 10, "Improvement Suggestions", ln=True)
    pdf.set_font("DejaVu", style="", size=12)
    
    if "suggestions" in analysis and analysis["suggestions"]:
        for suggestion in analysis["suggestions"]:
            # Use multi_cell for longer text and replace bullet points with hyphens
            pdf.multi_cell(0, 8, f"- {suggestion}")
            pdf.ln(5)
    
    # Save the PDF
    pdf.output(output_path)
    return output_path
