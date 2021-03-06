"""Get zipcodes."""

import urllib
import re
from bs4 import BeautifulSoup

ROOT_URL = "http://www.aip2.com/zip.htm"


def state_to_zipcodes(state_url):
    """get state zipcodes."""
    html = urllib.request.urlopen(state_url).read()
    regex = re.compile('[0-9]{5}', re.IGNORECASE | re.DOTALL)
    zips = regex.findall(html)
    assert len(zips) > 25
    return zips


def write_zips(zips):
    """Write zipcodes."""
    file = open('zipcodes.txt', 'a+')
    for zipcode in zips:
        file.write(str(zipcode)+'\r\n')
    file.close()


def extract_states(url):
    """get states."""
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    state_urls = [tag['href'] for tag in soup.findAll() if tag.getText()
                  and tag.getText()[0] == '[' and tag.getText()[-1] == ']'
                  and tag.name == 'a']
    for state_url in state_urls[2:]:
        zips = state_to_zipcodes(state_url)
        write_zips(zips)
        print('zipcodes finished and written for {}'.format(state_url))

if __name__ == '__main__':
    extract_states(ROOT_URL)
