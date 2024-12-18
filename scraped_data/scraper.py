import re
import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Function to extract <h3> elements with "question" in the ID
def extract_h3_with_question(url, key=""):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <h3> elements with "question" in the ID
        h3_elements = soup.find_all('h3', id=lambda x: x and key in x.lower())
        
        # Extract text and ID of each <h3>
        result = [{"id": h3['id'], "text": h3.get_text(strip=True)} for h3 in h3_elements]
        
        return result
    
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def extract_text_after_pattern(input_list):
    """
    Extracts text after the pattern:
    - "Question X:" or "X." or "X:" (number + special character with optional spaces).
    
    Args:
        input_list (list): List of input strings to process.
        
    Returns:
        list: A list of extracted strings.
    """
    extracted_texts = []
    
    # Regular expression to match:
    # - "Question X:" or "X." or "X:" (with or without spaces after the special character).
    pattern = r"^(?:Question\s*)?\d+[.:]\s*(.+)"  # Handles optional spaces after [.:]
    
    for item in input_list:
        match = re.match(pattern, item)
        if match:
            extracted_texts.append(match.group(1))  # Extract the text after the pattern
        else:
          extracted_texts.append(item)
    
    return extracted_texts


def write_to_text_file(text_list, filename="output.txt"):
    """
    Writes a list of strings to a text file, each string on a new line.
    
    Args:
        text_list (list): List of strings to write to the file.
        filename (str): Name of the output text file (default: "output.txt").
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in text_list:
                file.write(line + '\n')
        print(f"Successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def write_to_pdf(text_list, filename="output.pdf"):
    """
    Writes a list of strings to a PDF file, each string on a new line.
    
    Args:
        text_list (list): List of strings to write to the PDF.
        filename (str): Name of the output PDF file (default: "output.pdf").
    """
    try:
        # Create a canvas object with the given filename
        pdf = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Set initial coordinates for text
        x, y = 50, height - 50  # Start at the top-left margin
        
        # Loop through each line and add it to the PDF
        for line in text_list:
            pdf.drawString(x, y, line)
            y -= 20  # Move down the page for the next line
            
            # If y-coordinate is too low, create a new page
            if y < 50:
                pdf.showPage()
                y = height - 50
        
        # Save the PDF
        pdf.save()
        print(f"Successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to PDF: {e}")

if __name__ == "__main__":
    total_questions = list()
    # Example usage
    urls = ["https://www.geeksforgeeks.org/common-interview-questions-and-answers/",
            "https://www.geeksforgeeks.org/interview-preparation/",
            
            ]
    for url in urls:
        h3_questions = extract_h3_with_question(url, key='question')

        if h3_questions:
            for item in h3_questions:
                total_questions.append(item['text'])
        else:
            print("No matching <h3> elements found.")

    result = extract_text_after_pattern(total_questions)
    print("Text Extracted")

    write_to_pdf(result)