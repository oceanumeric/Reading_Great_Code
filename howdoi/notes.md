## Learning howdoi

Resources: https://mkaz.blog/code/python-argparse-cookbook/


### Example 1
```python
import sys


if __name__ == '__main__':
    print(sys.argv[0])
        try: 
            if sys.argv[1] == 'a':
                print('Lovely, you made it')
        except:
            None
```

In the terminal, run:
```bash
$ python3 notes.py a 
```

### Example 2 
```python
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
                        default=1, type=IntRange(1, 20))
    return parser


if __name__ == '__main__':
    parser = get_parser()
    print(parser.parse_args())  # no need to use sys.argv
```

In the terminal, run:
```bash
$ python3 notes.py a 
```

### Example 3
Python has a set of built-in methods and `__call__` is one of them. 
The `__call__` method enables Python programmers to write classes where the 
instances behave like functions and can be called like a function. When the 
instance is called as a function; if this method is defined, x(arg1, arg2, ...) 
is a shorthand for `x.__call__(arg1, arg2, ...)`.
```python
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



if __name__ == '__main__':
    ir = IntRange(1, 10)
    print(ir(19.9))
    print(IntRange(1, 10))

```

### Example 4 
```python
def foo_solution(data, n):
    '''
    This is for the question I got from foobar challenge with google 
    when I am working on this project. 
    '''
    # input: data-a list of integers
    # n: an integer 
    # output: a list filtered the repeated elements
    data_set = set(data)
    elements_remove = [e for e in data_set if data.count(e) > n]
    for e in elements_remove:
        while e in data:
            data.remove(e)
    return data

temp = [1, 2, 2, 2, 3, 4, 3]
solution = foo_solution(temp, 0)
print(solution)
```

### Example 5
The `vars()` function returns the `__dict__` attribute of the given object.
```python
class Foo:
  def __init__(self, a = 5, b = 10):
    self.a = a
    self.b = b
  
object = Foo()
print(vars(object))

{'a': 5, 'b': 10}
```

### Example 6
`isinstance(object, classinfo)`
Return True if the object argument is an instance of the classinfo argument, or 
of a (direct, indirect or virtual) subclass thereof. If object is not an object 
of the given type, the function always returns False. If classinfo is a tuple 
of type objects (or recursively, other such tuples), return True if object is 
an instance of any of the types. If classinfo is not a type or tuple of types 
and such tuples, a TypeError exception is raised.
```python
class Foo:
  def __init__(self, a = 5, b = 10):
    self.a = a
    self.b = b
  
object = Foo()
print(isinstance(object, str))
print(isinstance('aa', str))
print(isinstance(object, Foo))
```

### Example 7
`os.getenv(key, default=None)` method in Python returns the value of the environment variable key 
if it exists otherwise returns the default value.
```python
key = 'HOME'
print(os.getenv(key))  # '/home/michael'
```

### Example 8
Have you ever noticed that some URLs start with `http://`, while others start 
with `https://`? But where'd that extra "s" come from, and what does it mean?

SSL certificates are a small data files that cryptographically establish an 
encrypted link between a web server and a browser. This link ensures that all 
data passed between the web server and browser remain private.


### Example 9 
The inspect module provides several useful functions to help get information 
about live objects such as modules, classes, methods, functions, tracebacks, 
frame objects, and code objects. For example, it can help you examine the 
contents of a class, retrieve the source code of a method, extract and format 
the argument list for a function, or get all the information you need to 
display a detailed traceback.
```python
# import required modules
import inspect
  
# explicit function
def fun(a):
    return 2*a
  
# use isfunction()
print(inspect.isfunction(fun))
```

### Example 10
 The Session object allows you to persist certain parameters across requests. It also persists cookies across all requests made from the Session instance, and will use `urllib`’s connection pooling. So if you’re making several requests to the same host, the underlying TCP connection will be reused, which can result in a significant performance increase


 ## Example 11
 ```python
 from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
 ```


 ### Example 12
 `os.urandom()` method is used to generate a string of size random bytes suitable 
 for cryptographic use or we can say this method generates a string 
 containing random characters.
 ```python
 # importing os module 
import os 
      
# Declaring size
size = 5
  
# Using os.urandom() method
result = os.urandom(size) 
      
# Print the random bytes string
# Output will be different everytime 
print(result) 
# output: b'\xe2\xaf\xbc:\xdd'
 ```