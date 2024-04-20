from bs4 import BeautifulSoup
import requests

# URL of the webpage containing the input element
url = 'https://twitter.com/home'

# Fetch the HTML content of the webpage
response = requests.get(url)
html_content = response.text

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)
# Find the input element with the name "email"
email_input = soup.find('input', {'name': 'email'})

# Check if the input element is found
if email_input:
    print("Input element with name 'email' found:")
    print(email_input)
else:
    print("Input element with name 'email' not found on the webpage.")
