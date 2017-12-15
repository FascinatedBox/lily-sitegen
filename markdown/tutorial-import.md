@title: Import

Lily's import system borrows mostly from Python, notably how the module name is
used as a namespace for the symbols inside:

```
# fib.lily

define fib(n: Integer): Integer
{
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
}

# other.lily

import fib

# print(fib(10)) # Syntax error

print(fib.fib(10)) # 55
```

If a module executes code, the code is run only the first time the module is
loaded.

### Import as

It is possible to rename modules using the `as` keyword:

```
import fib as f

print(f.fib(10)) # 55

# print(fib.fib(10)) # Syntax error because fib isn't available.
```

To extract only particular symbols from a module (and not the module itself),
use `(<name>, <name>...)` before the import name. The module will be loaded, but
not made visible (only the symbols mentioned will be).

```
import (argv, getenv) sys

print(argv)
print(getenv("HOME"))
```

### Import symbols

It is possible to import only certain symbols from a module. The code inside a
module (if any) will still execute, but only the items in question will be
available.

Use `(name1, name2, ...)` before the module name. This **cannot** be used with
`import x as y`.

```
import (argv, getenv) sys

print(getenv("HOME")) # Returns the home path

# print(sys.argv) # Syntax error because 'sys' is not loaded.
```

### Import Multiple

Commas can be used to execute multiple import actions at once:

```
import fib as f,
       sys,
       (Time) time
```

The code inside of a module is only executed the first time that it is imported:

```
# print_one.lily

print(1)

# other.lily

import print_one

# main.lily

import print_one # prints 1
import other # Does nothing.
```

### Import String

To import a file from another directory, the path must be enclosed in quotes.
The `/` character is used to denote path slashes, and will be turned into the
appropriate character on platforms that do not use `/`.

```
# somedir/point.lily

class Point(var @x: Integer, var @y: Integer)
{
    public define stringified: String {
        return "Point({0}, {1})".format(@x, @y)
    }
}

# first.lily

import "somedir/point"

print(point.Point(10, 20).stringified())
```
