import PyPDF2
from fpdf import FPDF
import os
import datetime

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
    
    # Now create a more visually appealing PDF
    try:
        class PDF(FPDF):
            def header(self):
                # Header with gradient
                self.set_fill_color(67, 97, 238)  # Primary color
                self.rect(0, 0, 210, 25, 'F')
                self.set_fill_color(114, 9, 183)  # Secondary color
                self.rect(0, 20, 210, 8, 'F')
                
                # Logo or title
                self.set_font('Courier', 'B', 20)
                self.set_text_color(255, 255, 255)
                self.cell(0, 20, 'ENHANCED RESUME ANALYSIS', 0, 1, 'C')
                
                # Add date
                self.set_font('Courier', '', 10)
                self.set_text_color(255, 255, 255)
                current_date = datetime.datetime.now().strftime("%B %d, %Y")
                self.cell(0, 8, f'Generated on: {current_date}', 0, 1, 'R')
                
                # Add some space after header
                self.ln(15)
            
            def footer(self):
                # Footer
                self.set_y(-15)
                self.set_font('Courier', 'I', 8)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
                self.cell(0, 10, 'Powered by Gemini AI | Created by Learnershakil', 0, 0, 'R')
        
        # Create new PDF instance
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # If there's a name in personal info, add it prominently
        if "personal_info" in analysis and "name" in analysis["personal_info"]:
            pdf.set_font('Courier', 'B', 18)
            pdf.set_text_color(67, 97, 238)  # Primary color
            pdf.cell(0, 10, sanitize_text(analysis["personal_info"]["name"]), 0, 1, 'C')
            pdf.ln(5)
        
        # Add personal information in a nice box
        pdf.set_font('Courier', 'B', 14)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(67, 97, 238)  # Primary color
        pdf.cell(0, 10, sanitize_text("Personal Information"), 0, 1, 'L', 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Courier', '', 12)
        
        if "personal_info" in analysis:
            for key, value in analysis["personal_info"].items():
                if key != "name":  # Skip name as we already displayed it
                    pdf.set_font('Courier', 'B', 11)
                    pdf.cell(40, 8, sanitize_text(f"{key.capitalize()}:"), 0)
                    pdf.set_font('Courier', '', 11)
                    pdf.cell(0, 8, sanitize_text(f"{value}"), 0, 1)
        
        # Add skills section with colored bullets
        pdf.ln(5)
        pdf.set_font('Courier', 'B', 14)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(114, 9, 183)  # Secondary color
        pdf.cell(0, 10, sanitize_text("Skills"), 0, 1, 'L', 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Courier', '', 11)
        
        if "skills" in analysis and analysis["skills"]:
            pdf.ln(2)
            # Create a multi-column layout for skills
            skill_x = pdf.get_x()
            skill_y = pdf.get_y()
            max_y = skill_y
            col_width = 95
            skill_count = len(analysis["skills"])
            half_count = (skill_count + 1) // 2
            
            for i, skill in enumerate(analysis["skills"]):
                if i == half_count:
                    skill_x = skill_x + col_width
                    pdf.set_xy(skill_x, skill_y)
                
                pdf.set_text_color(67, 97, 238)  # Primary color for bullet
                pdf.cell(5, 8, "* ", 0, 0)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 8, sanitize_text(skill), 0, 1)
                max_y = max(max_y, pdf.get_y())
                
                if i < half_count - 1 or i >= half_count:
                    pdf.set_xy(skill_x, pdf.get_y())
                else:
                    pdf.set_xy(skill_x, skill_y)
            
            pdf.set_y(max_y + 5)
        
        # Add education section with timeline visualization
        pdf.ln(5)
        pdf.set_font('Courier', 'B', 14)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(76, 201, 240)  # Accent color
        pdf.cell(0, 10, sanitize_text("Education"), 0, 1, 'L', 1)
        pdf.set_text_color(0, 0, 0)
        
        if "education" in analysis and analysis["education"]:
            for edu in analysis["education"]:
                if isinstance(edu, dict):
                    # Draw timeline dot
                    current_y = pdf.get_y()
                    pdf.set_fill_color(76, 201, 240)  # Accent color
                    pdf.circle(15, current_y + 5, 2, 'F')
                    pdf.line(15, current_y + 7, 15, current_y + 20)
                    
                    # Education details
                    pdf.set_xy(20, current_y)
                    pdf.set_font('Courier', 'B', 12)
                    pdf.cell(0, 8, sanitize_text(edu.get("degree", "")), 0, 1)
                    pdf.set_font('Courier', '', 10)
                    pdf.set_x(20)
                    pdf.cell(0, 6, sanitize_text(edu.get("institution", "")), 0, 1)
                    
                    # Year with background
                    if "year" in edu:
                        pdf.set_x(20)
                        pdf.set_fill_color(242, 242, 242)
                        pdf.set_text_color(67, 97, 238)
                        pdf.cell(30, 6, sanitize_text(edu["year"]), 0, 1, 'L', 1)
                        pdf.set_text_color(0, 0, 0)
                    
                    # Details if available
                    if "details" in edu and edu["details"]:
                        pdf.set_x(20)
                        pdf.set_font('Courier', 'I', 10)
                        pdf.multi_cell(170, 6, sanitize_text(edu["details"]))
                    
                    pdf.ln(5)
                else:
                    pdf.set_x(20)
                    pdf.cell(0, 8, sanitize_text(f"- {edu}"), 0, 1)
        
        # Add experience section
        pdf.ln(5)
        pdf.set_font('Courier', 'B', 14)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(247, 37, 133)  # Secondary accent color
        pdf.cell(0, 10, sanitize_text("Experience"), 0, 1, 'L', 1)
        pdf.set_text_color(0, 0, 0)
        
        if "experience" in analysis and analysis["experience"]:
            for exp in analysis["experience"]:
                if isinstance(exp, dict):
                    # Draw timeline dot
                    current_y = pdf.get_y()
                    pdf.set_fill_color(247, 37, 133)  # Secondary accent color
                    pdf.circle(15, current_y + 5, 2, 'F')
                    pdf.line(15, current_y + 7, 15, current_y + 20)
                    
                    # Experience details
                    pdf.set_xy(20, current_y)
                    pdf.set_font('Courier', 'B', 12)
                    pdf.cell(0, 8, sanitize_text(exp.get("position", "")), 0, 1)
                    pdf.set_font('Courier', '', 10)
                    pdf.set_x(20)
                    pdf.cell(0, 6, sanitize_text(exp.get("company", "")), 0, 1)
                    
                    # Duration with background
                    if "duration" in exp:
                        pdf.set_x(20)
                        pdf.set_fill_color(242, 242, 242)
                        pdf.set_text_color(247, 37, 133)
                        pdf.cell(60, 6, sanitize_text(exp["duration"]), 0, 1, 'L', 1)
                        pdf.set_text_color(0, 0, 0)
                    
                    # Details if available
                    if "details" in exp and exp["details"]:
                        pdf.set_x(20)
                        pdf.set_font('Courier', '', 10)
                        pdf.multi_cell(170, 6, sanitize_text(exp["details"]))
                    
                    pdf.ln(5)
                else:
                    pdf.set_x(20)
                    pdf.cell(0, 8, sanitize_text(f"- {exp}"), 0, 1)
        
        # Add suggestions on a new page with stylized design
        pdf.add_page()
        
        # Title for suggestions
        pdf.set_font('Courier', 'B', 16)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(67, 97, 238)  # Primary color
        pdf.cell(0, 12, sanitize_text("RECOMMENDATIONS TO IMPROVE YOUR RESUME"), 0, 1, 'C', 1)
        pdf.ln(10)
        
        # Introduction to suggestions
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Courier', 'I', 11)
        pdf.multi_cell(0, 6, sanitize_text("Based on our AI analysis, here are personalized suggestions to enhance your resume and improve your job prospects:"))
        pdf.ln(5)
        
        # Add suggestions with numbered bullets and background
        if "suggestions" in analysis and analysis["suggestions"]:
            for i, suggestion in enumerate(analysis["suggestions"], 1):
                # Number circle
                pdf.set_fill_color(67, 97, 238)  # Primary color
                pdf.set_text_color(255, 255, 255)
                pdf.circle(15, pdf.get_y() + 5, 5, 'F')
                pdf.set_xy(12, pdf.get_y() + 2)
                pdf.set_font('Courier', 'B', 10)
                pdf.cell(6, 6, str(i), 0, 0, 'C')
                
                # Suggestion text
                pdf.set_font('Courier', '', 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_xy(25, pdf.get_y())
                
                # Background for suggestion
                suggestion_y = pdf.get_y()
                clean_suggestion = sanitize_text(suggestion)
                
                # Calculate height needed for text
                temp_x = pdf.get_x()
                temp_y = pdf.get_y()
                pdf.set_xy(25, suggestion_y)
                pdf.multi_cell(165, 6, clean_suggestion, 0, 'L')
                suggestion_height = pdf.get_y() - suggestion_y
                pdf.set_xy(temp_x, temp_y)  # Restore position
                
                # Draw background and left border for suggestion
                pdf.set_fill_color(242, 242, 242)
                pdf.rect(25, suggestion_y, 165, suggestion_height, 'F')
                pdf.set_draw_color(67, 97, 238)
                pdf.set_line_width(1)
                pdf.line(25, suggestion_y, 25, suggestion_y + suggestion_height)
                
                # Draw text over background
                pdf.set_xy(28, suggestion_y)
                pdf.multi_cell(162, 6, clean_suggestion)
                
                pdf.ln(8)
        
        # Final note and summary
        pdf.ln(5)
        pdf.set_font('Courier', 'I', 10)
        pdf.multi_cell(0, 6, sanitize_text("Implementing these suggestions can significantly improve your resume's effectiveness and increase your chances of landing interviews. Focus on highlighting your strengths and tailoring your resume to specific job opportunities."))
        
        # Conclusion with call to action
        pdf.ln(10)
        pdf.set_fill_color(76, 201, 240)  # Accent color
        pdf.rect(10, pdf.get_y(), 190, 25, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, pdf.get_y() + 5)
        pdf.set_font('Courier', 'B', 12)
        pdf.cell(0, 6, "NEXT STEPS:", 0, 1)
        pdf.set_font('Courier', '', 10)
        pdf.set_x(15)
        pdf.multi_cell(180, 6, "1. Update your resume based on these suggestions\n2. Tailor it for specific job applications\n3. Have someone review your revised resume")
        
        # Save the PDF
        pdf.output(output_path)
        return output_path
    except Exception as e:
        print(f"Error generating enhanced PDF: {e}")
        # Return the text file path as fallback
        return text_output_path
