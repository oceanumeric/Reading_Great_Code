import argparse
import textwrap
import sys


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
