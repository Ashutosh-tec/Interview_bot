import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Function to extract <h3> elements with "question" in the ID
# Function to extract <div> elements with a specific class and format text
def extract_div_with_class(url, class_name="text"):
    """
    Extracts the visible text content of <div> elements with a specific class, formatted with line breaks.
    
    Args:
        url (str): The URL of the webpage to scrape.
        class_name (str): The class name of the <div> elements to extract.
        
    Returns:
        list: A list of strings containing the text content of matching <div> elements, formatted properly.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <div> elements with the specified class
        div_elements = soup.find_all('div', class_=class_name)
        
        # Extract and clean text content from each <div>, preserving formatting
        content = [div.get_text(separator="\n", strip=True) for div in div_elements]

        return content

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def write_to_pdf(text_list, filename="output.pdf", max_width=480):
    """
    Writes a list of strings to a PDF file, wrapping text if it exceeds the max width.

    Args:
        text_list (list): List of strings to write to the PDF.
        filename (str): Name of the output PDF file (default: "output.pdf").
        max_width (int): Maximum width of the text before wrapping (default: 450).
    """
    try:
        # Create a canvas object with the given filename
        pdf = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Set initial coordinates for text
        x, y = 50, height - 50  # Start at the top-left margin
        line_height = 15  # Height of each line of text

        # Loop through each line in the text list
        for line in text_list:
            # Split the line into chunks that fit within the max width
            words = line.split()
            wrapped_lines = []
            current_line = ""
            for word in words:
                if pdf.stringWidth(current_line + " " + word) <= max_width:
                    current_line += " " + word
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line.strip())

            # Draw each wrapped line on the PDF
            for wrapped_line in wrapped_lines:
                pdf.drawString(x, y, wrapped_line)
                y -= line_height
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
    # Example usage
    urls = ["https://www.geeksforgeeks.org/common-interview-questions-and-answers/",
            ]
            # "https://www.geeksforgeeks.org/interview-preparation/"  
    class_name = "text"  
    for url in urls:
        div_content = extract_div_with_class(url, class_name)
        total_text = list()

        if div_content:
            print(f"Extracted content from <div> elements with class '{class_name}':\n")
            for txt in div_content:
                for index, text in enumerate(txt.split('\n'), start=1):
                    if len(text) > 3:
                        total_text.append(text)
            write_to_pdf(total_text, "output.pdf")
        else:
            print(f"No <div> elements with class '{class_name}' found.")