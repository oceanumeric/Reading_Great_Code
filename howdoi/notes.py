import argparse
import sys

# resources
# https://mkaz.blog/code/python-argparse-cookbook/

## Example 1

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print(args.accumulate(args.integers))

## Example 2

# if len(sys.argv) > 3:
#     print('You have specified too many arguments')
#     sys.exit()

# if len(sys.argv) < 2:
#     print('You need to specify the path to be listed')
#     sys.exit()

# input_value0, input_value1 = sys.argv[0], sys.argv[1]

# print(input_value0, input_value1)

## Example 3

# create a parser
parser = argparse.ArgumentParser(
    description='Demostration of parse in Python'
)
# add an argument
parser.add_argument(
    'namefp',   # it will become positional argument without --
    metavar="fp", 
    type=str,
    help='Print the first input'
)

parser.add_argument(
    '--verbose',
    action='store_true',
    help='Conditional print'
)

parser.add_argument(
    '-list',
    nargs=2,
    type=int # it will be a list of str if no type was specified
)

parser.add_argument(
    '-str',
    nargs='*',  # it will accept all arguments 
)

parser.add_argument(
    '--sum',
    nargs='*',
    type=int,
    help="Return the sum of all intergers after it"
)

# Execute the parse_args() method
args = parser.parse_args()
input_value0 = args.namefp

if args.verbose:  # args.ingore -- 
    print('haha, very verbose')
else:
    print('no verbose argument passed')

print(input_value0, args.list, args.str, sum(args.sum))