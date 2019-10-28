from .models import Quote
import requests

def get_quotes():
   '''
   Function that gets the json response to our url request
   '''
   get_quote_response = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
   print(get_quote_response)
   return get_quote_response