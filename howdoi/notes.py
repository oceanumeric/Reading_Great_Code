import argparse
import textwrap
import os
import sys
import inspect
import logging 
import appdirs
from cachelib import FileSystemCache, NullCache


if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
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

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

CACHE_EMPTY_VAL = 'NULL'
CACHE_DIR = appdirs.user_cache_dir('howdoi')
CACHE_ENTRY_MAX = 128

if os.getenv('HOWDOI_DISABLE_CACHE'):
    # works like an always empty cache
    cache = NullCache()
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)


class IntRange:
    def __init__(self, imin=None, imax=None) -> None:
        self.imin = imin
        self.imax = imax
        
    def __call__(self, arg):
        try:
            value = int(arg)
        except ValueError as value_error:
            raise self.exception() from value_error
        if (self.imin is not None 
            and value < self.imin) or (self.imax is not None 
                                       and value > self.imax):
            raise self.exception()
        return value
            
    def exception(self):
        if self.imin is not None and self.imax is not None:
            return argparse.ArgumentTypeError(
                f'Must be an integer in the range [{self.imin}, {self.imax}]'
                )
        if self.imin is not None:
            return argparse.ArgumentTypeError(f'Must be an integer >= {self.imin}')
        if self.imax is not None:
            return argparse.ArgumentTypeError(f'Must be an integer <= {self.imax}')
        return argparse.ArgumentTypeError('Must be an integer')
            

def get_parser():
    parser = argparse.ArgumentParser(
        description='instant coding answers via the command line',
        epilog=textwrap.dedent('''\
            environment variable examples:
                HOWDOI_COLORIZE=1
                HOWDOI_DISABLE_CACHE=1
                HOWDOI_DISABLE_SSL=1
                HOWDOI_SEARCH_ENGINE=google
                HOWDOI_URL=serverfault.com
            '''),
            formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*', 
                        help='the question to answer')
    parser.add_argument('-p', '--pos', 
                        help='select answer in specified postion (default: 1)',
                        default=1, type=IntRange(1, 20), metavar='POS')
    parser.add_argument('-n', '--num', 
                        help='number of answers to return (default: 1)',
                        dest='num_answers', default=1, type=IntRange(1, 20), 
                        metavar='NUM')
    parser.add_argument('--num-answers', help=argparse.SUPPRESS)
    parser.add_argument('-a', '--all', 
                        help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l', '--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output',
                        action='store_true')
    parser.add_argument('-x', '--explain', help='explain how answer was chosen',
                        action='store_true')
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('-j', '--json', help='return answers in raw json format',
                        dest='json_output',
                        action='store_true')
    parser.add_argument('--json-output', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('-v', '--version',
                        help='display the current version of howdoi',
                        action='store_true')
    parser.add_argument('-e', '--engine',
                        help='search engine for this query \
                            (google, bing, duckduckgo)',
                        dest='search_engine', nargs="?",
                        metavar='ENGINE')
    parser.add_argument('--save', '--stash', help='stash a howdoi answer',
                        action='store_true')
    parser.add_argument('--view', help='view your stash',
                        action='store_true')
    parser.add_argument('--remove', help='remove an entry in your stash',
                        action='store_true')
    parser.add_argument('--empty', help='empty your stash',
                        action='store_true')
    parser.add_argument('--sanity-check', help=argparse.SUPPRESS,
                        action='store_true')
    return parser


def _get_answers(args, link):
    """
    @args: command-line arguments
    returns: array of answers and their respective metadata
             False if unable to get answers
    """
    questions_links = _get_links_with_cache(args['query'])

    
def _get_links_with_cache(query):
    cache_key = _get_cache_key(query)
    res = _get_from_cache(cache_key)
    if res:
        logging.info('Using cached links')
        if res ==  CACHE_EMPTY_VAL:
            logging.info('No StackOverflow links found in cached search \
                engine results - will make live query')
        else:
            return res
    
    
def _get_from_cache(cache_key):
    # as of cachelib 0.3.0, it internally logging a warning on cache miss
    current_log_level = logging.getLogger().getEffectiveLevel()
    # reduce the log level so that warning is not printed
    logging.getLogger().setLevel(logging.ERROR)
    page = cache.get(cache_key)
    logging.getLogger().setLevel(current_log_level)
    return page
    
    
def _get_cache_key(args):
    frame = inspect.currentframe()
    calling_func = inspect.getouterframes(frame)[1].function
    return calling_func + str(args) +  '2.0.18'

def _get_search_url(search_engine):
    return SEARCH_URLS.get(search_engine, SEARCH_URLS['google'])

def _get_links(query):
    search_engine = os.getenv('HOWDOI_SEARCH_ENGINE', 'google')
    search_url = _get_search_url(search_engine).format(URL, )


if __name__ == '__main__':
    print(sys.argv[0])
    try: 
        if sys.argv[1] == 'a':
            print('Lovely, you made it')
    except:
        None
    parser = get_parser()
    args = vars(parser.parse_args())
    print(args)
    args = vars(parser.parse_args('how do i sd -p 2 -n 9 -x'.split(' ')))
    print(args)
    print(os.getenv('HOWDOI_SEARCH_ENGINE', 'google'))
    gck = _get_cache_key(args)
    print(gck)
