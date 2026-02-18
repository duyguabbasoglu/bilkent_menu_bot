import requests
from bs4 import BeautifulSoup

url = "https://bais.bilkent.edu.tr/menu/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all menu containers
# Based on grep, looked like "Tabildot Fiks Menü" was in h5 or similar?
# Let's find all text containing "Fiks" and print parent structure

for element in soup.find_all(string=lambda text: text and "Fiks" in text):
    print(f"\n--- Found: {element.strip()} ---")
    parent = element.parent
    # Print a bit of the structure
    print(parent.prettify()[:500])
    
    # Try to find the siblings which contain the food items
    # Usually in a table or list below the header
    
    # Traverse up to find the container
    container = parent.find_parent('div', class_='card') # Guessing 'card' based on grep
    if container:
        print("\n--- Container Content ---")
        print(container.get_text(separator=' | ', strip=True)[:500])
