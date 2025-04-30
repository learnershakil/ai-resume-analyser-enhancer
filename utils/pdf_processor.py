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
    # First try to create a text version as a reliable fallback
    text_output_path = output_path.replace('.pdf', '.txt')
    try:
        with open(text_output_path, 'w') as f:
            f.write("ENHANCED RESUME ANALYSIS\n\n")
            
            # Personal info section
            f.write("PERSONAL INFORMATION\n")
            f.write("-------------------\n")
            if "personal_info" in analysis:
                for key, value in analysis["personal_info"].items():
                    f.write(f"{key.capitalize()}: {value}\n")
            f.write("\n")
            
            # Skills section
            f.write("SKILLS\n")
            f.write("------\n")
            if "skills" in analysis and analysis["skills"]:
                for skill in analysis["skills"]:
                    f.write(f"- {skill}\n")
            f.write("\n")
            
            # Education section
            f.write("EDUCATION\n")
            f.write("---------\n")
            if "education" in analysis and analysis["education"]:
                for edu in analysis["education"]:
                    if isinstance(edu, dict):
                        for key, value in edu.items():
                            f.write(f"{key}: {value}\n")
                        f.write("\n")
                    else:
                        f.write(f"- {edu}\n")
            f.write("\n")
            
            # Experience section
            f.write("EXPERIENCE\n")
            f.write("----------\n")
            if "experience" in analysis and analysis["experience"]:
                for exp in analysis["experience"]:
                    if isinstance(exp, dict):
                        for key, value in exp.items():
                            f.write(f"{key}: {value}\n")
                        f.write("\n")
                    else:
                        f.write(f"- {exp}\n")
            f.write("\n")
            
            # Suggestions section
            f.write("IMPROVEMENT SUGGESTIONS\n")
            f.write("-----------------------\n")
            if "suggestions" in analysis and analysis["suggestions"]:
                for i, suggestion in enumerate(analysis["suggestions"], 1):
                    f.write(f"{i}. {suggestion}\n\n")
    except Exception as e:
        print(f"Error creating text fallback file: {e}")
    
    # Helper function to sanitize text for PDF
    def sanitize_text(text):
        if not isinstance(text, str):
            text = str(text)
        # Replace problematic characters
        replacements = {
            "'": "'",
            """: '"',
            """: '"',
            "–": "-",
            "—": "-",
            "'": "'",
            "•": "-",
            "\u2022": "-",  # bullet
            "\u2018": "'",  # left single quote
            "\u2019": "'",  # right single quote
            "\u201C": '"',  # left double quote
            "\u201D": '"',  # right double quote
            "\u2013": "-",  # en dash
            "\u2014": "-",  # em dash
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    # Now try to create the PDF
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Use standard fonts
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 10, sanitize_text("Enhanced Resume Analysis"), ln=True, align="C")
        pdf.ln(10)
        
        # Add personal information
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, sanitize_text("Personal Information"), ln=True)
        pdf.set_font("Courier", "", 12)
        
        if "personal_info" in analysis:
            for key, value in analysis["personal_info"].items():
                pdf.cell(0, 8, sanitize_text(f"{key.capitalize()}: {value}"), ln=True)
        
        # Add skills section
        pdf.ln(5)
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, sanitize_text("Skills"), ln=True)
        pdf.set_font("Courier", "", 12)
        
        if "skills" in analysis and analysis["skills"]:
            for skill in analysis["skills"]:
                pdf.cell(0, 8, sanitize_text(f"- {skill}"), ln=True)
        
        # Add education section
        pdf.ln(5)
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, sanitize_text("Education"), ln=True)
        pdf.set_font("Courier", "", 12)
        
        if "education" in analysis and analysis["education"]:
            for edu in analysis["education"]:
                if isinstance(edu, dict):
                    for key, value in edu.items():
                        pdf.cell(0, 8, sanitize_text(f"{key}: {value}"), ln=True)
                    pdf.ln(5)
                else:
                    pdf.cell(0, 8, sanitize_text(f"- {edu}"), ln=True)
        
        # Add experience section
        pdf.ln(5)
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, sanitize_text("Experience"), ln=True)
        pdf.set_font("Courier", "", 12)
        
        if "experience" in analysis and analysis["experience"]:
            for exp in analysis["experience"]:
                if isinstance(exp, dict):
                    for key, value in exp.items():
                        pdf.cell(0, 8, sanitize_text(f"{key}: {value}"), ln=True)
                    pdf.ln(5)
                else:
                    pdf.cell(0, 8, sanitize_text(f"- {exp}"), ln=True)
        
        # Add suggestions
        pdf.add_page()
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, sanitize_text("Improvement Suggestions"), ln=True)
        pdf.set_font("Courier", "", 12)
        
        if "suggestions" in analysis and analysis["suggestions"]:
            for i, suggestion in enumerate(analysis["suggestions"], 1):
                clean_suggestion = sanitize_text(suggestion)
                pdf.multi_cell(0, 8, sanitize_text(f"{i}. {clean_suggestion}"))
                pdf.ln(5)
        
        # Save the PDF
        pdf.output(output_path)
        return output_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Return the text file path as fallback
        return text_output_path
