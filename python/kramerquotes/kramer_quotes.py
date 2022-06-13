# Simple script to get kramer quotes and dump them to a file
import requests
from bs4 import BeautifulSoup

BASEURL = "https://quotecatalog.com/communicator/cosmo-kramer/"

# function to scrape baseurl
def get_quotes():
    # get the html
    html = requests.get(BASEURL)
    # parse the html
    soup = BeautifulSoup(html.text, "html.parser")
    # find the quotes
    quotes = soup.find_all(
        "a", class_="block p-5 font-serif md:text-lg quoteCard__blockquote"
    )
    # loop through the quotes

    print("Writing quotes to file...")
    for quote in quotes:
        # get the quote text
        quote_text = quote.contents[0]

        # strip non whitespace characters from the start and end of the quote
        quote_text = quote_text.strip()

        # write the quote to a file as json
        with open("quotes.txt", "a") as f:
            f.write(quote_text + "\n")
    print("Quotes written to file.")


if __name__ == "__main__":
    get_quotes()
