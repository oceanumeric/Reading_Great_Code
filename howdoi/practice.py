import logging
import os
import requests
import sys 
from urllib.request import getproxies
from urllib.parse import quote as url_quote


BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
UNDERLINE = '\033[4m'
END_FORMAT = '\033[0m'  # append to string to end text formatting.

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) \
    Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) \
                   Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) \
                   Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) \
                   AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 \
                   (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'),)

DISABLE_SSL = True

if DISABLE_SSL:  # Set http instead of https
    SCHEME = 'http://'
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = 'https://'
    VERIFY_SSL_CERTIFICATE = True
    
SEARCH_URLS = {
    'bing': SCHEME + 'www.bing.com/search?q=site:{0}%20{1}&hl=en',
    'google': SCHEME + 'www.google.com/search?q=site:{0}%20{1}&hl=en',
    'duckduckgo': SCHEME + 'duckduckgo.com/html?q=site:{0}%20{1}&t=hj&ia=web'
}

search_session = requests.session()


def _random_int(width):
    # width: length of bytes 1bytes = 8 bit = 2^8 = 256
    bres = os.urandom(width)
    if sys.version < '3':
        ires = int(bres.encode('hex'), 16)
    else:
        ires = int.from_bytes(bres, 'little')
    
    return ires


def _random_choice(seq):
    return seq[_random_int(1) % len(seq)]


def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = f'http://{value}'
            else:
                 filtered_proxies[key] = value
        
    return filtered_proxies


def _get_search_url(search_engine):
    return SEARCH_URLS.get(search_engine, SEARCH_URLS['google'])
                 

def _get_result(url):
    try:
        resp = search_session.get(url,
                                  headers={
                                      'User-Agent': _random_choice(USER_AGENTS)
                                  },
                                  proxies=get_proxies(),
                                  verify=VERIFY_SSL_CERTIFICATE,
                                  cookies={'CONSENT': 'YES+US.en+20170717-00-0'}
                                  )
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.SSLError as error:
        logging.error(
            '%sEncountered an SSL Error. Try using HTTP instead of '
            'HTTPS by disabling SSL verification".\n%s', RED, END_FORMAT
        )
        raise error
        


if __name__ == '__main__':
    URL = 'stackoverflow.com'
    query = 'python list comprehension'
    search_engine = 'google'
    search_url = _get_search_url(search_engine).format(URL, url_quote(query))
    print(search_url)
    print(url_quote(query))