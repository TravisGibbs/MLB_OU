import string
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import json
from itertools import chain


data = json.load(open('./player_data.json'))
print(list(data.items())[:5])