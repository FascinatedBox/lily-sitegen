@title: Functions

In Lily, functions are first-class entities. They can be passed around as
arguments, returned, stored in vars, and so forth. There are several kinds of
functions in the language, as well as a handful of keywords that can augment
them.

The most common kind of function is a native function created through the
`define` keyword:

### define

```
# Function(Integer, Integer => Integer)
define add(left: Integer, right: Integer): Integer {
    return left + right
}
```

The above defines `add` as taking two `Integer` values and producing an
`Integer` as output.

In the event that a function has no arguments, or produces no output, that
entire section can be omitted:

```
# Function( => Integer)
define return_10: Integer {
    return 10
}

# Function(Integer)
define return_nothing(a: Integer) {
}

# Function()
define no_op {
}
```

Like many curly-brace family languages, functions are invoked by passing their
arguments like so: `add(5, 10)` to receive `15`.

Omitting a return type doesn't mean that a function doesn't return anything. A
function that doesn't mention a return value will actually the value `unit` of
the class `Unit`. Since all functions actually return a value (even if it's just
`unit`), it's possible to chain functions that otherwise could not be chained:

```
define no_op { }

print(no_op()) # unit
```

Functions can also be used as arguments:

```
define square(input: Integer): Integer {
    return input * input
}

define apply_action(a: Integer, fn: Function(Integer => Integer)): Integer
{
    return fn(a)
}

print(apply_action(10, square)) # 100
```

The `define` keyword has a number of modifiers that are available to it
( `public`, `forward`, `static`, etc. ). For simplicity, Lily requires that
modifiers are introduced in alphabetical order.

### Lambdas

One problem with the above example is that `square` is relatively simple. One
is likely to assume that `square` will take an input, multiply it by itself, and
return that input. But suppose that the codebase is large, and `square` is
somewhere else. If there is an issue, the source to `square` must be tracked
down.

An alternative is to use a lambda. Lambdas are nameless functions that can be
used where a function is needed. A lambda begins with `(|`, followed by argument
names, until `|` is seen. From there, everything until there is a matching `)`
for the `(|` is the body of the lambda. Here's the above, rewritten to use a
lambda.

```
define apply_action(a: Integer, fn: Function(Integer => Integer)): Integer
{
    return fn(a)
}

print(apply_action(10, (|a| a * a) )) # 100
```

Now the intent is much clearer, because `a` is being multiplied by itself.

Another feature of lambdas is that they are values, and the var they're assigned
to can opt to have a different lambda. On the other hand, lambdas are quite
restricted, and not eligible for many of the function features listed below.

Lambdas don't require type information. In the above example, the lambda uses
inference to determine that `a` should be of type `Integer`. Since lambdas
exist primarily to return some kind of a value, the return type of a lambda is
the last expression that run. If the last expression is part of a block such as
`if` or `match`, then the return type is instead `unit`.

### Closures

One limitation of the above kinds of declarations is that, outside of global
variables, they're limited strictly to what they've been given. This is where
closures come in handy.

Here's an example of a function that returns an ever-increasing `Integer`
value:

```
define get_counter: Function( => Integer) {
    var counter = 0

    define counter_fn: Integer {
        counter += 1
        return counter
    }

    return counter_fn
}

var c = get_counter()
var results = [c(), c(), c()]

print(results)
# Result:
# [0, 1, 2]
```

Lambdas can also be closures:

```
define list_total(l: List[Integer]): Integer {
    var total = 0

    l.each(|e| total += e )

    return total
}
```

The above would be much improved if it used generics to allow for any type of
`List`. Or, even better, if it used `List.fold` to avoid making a closure at
all.

### foreign

Foreign functions are functions that are introduced from a non-Lily library.
These functions, like those created by `define`, cannot be reassigned.

### Features

Functions in Lily have a number of different features available to them. All
function kinds except for lambdas can make use of all of these features.

#### forward

Using the `forward` keyword before `define` denotes that the function will be
declared at some point in the future. Instead of giving the `define` a body, it
must instead have the triple dot (`...`) token:

```
forward define add(Integer, Integer): Integer { ... }

# (more definitions)

define add(x: Integer, y: Integer): Integer {
    return x + y
}
```

Functions declared with `forward` are not allowed to specify names for their
variables, and are not allowed to use keyword arguments.

While there are unresolved forward declarations, it is a syntax error to attempt
to import a file, declare a class property, or declare a var. This is done to
prevent the resolving function from using variables that are not properly
initialized.

Additionally, if a class or module finishes with incomplete forward
declarations, a syntax error is generated immediately.

#### Varargs

Adding `...` to the end of a type denotes that the function can receive a
variable number of arguments of that type. The function receives the arguments
as a `List` of the type provided. If no arguments were passed, the `List` will
be empty.

```
# Function(Integer...) => Integer
define sum(numbers: Integer...): Integer
{
    var total = 0
    numbers.each(|e| total += e )
    return total
}

# sum() # 0
# sum(1, 2, 3) # 6
```

#### Optargs

Adding `*` before a type, then `= <value>` after it denotes that the parameter
is optional. Optional arguments may be a simple value, or an expression.
Required arguments must not come after an optional argument.

The expressions of optional arguments, if run, are always run from left to
right. As a result, it's permissible for a parameter to depend on another to the
left of it.

```
# Function(*Integer => Integer)
define optarg(a: *Integer = 10): Integer { return a + 10 }

optarg(100) # 110
optarg() # 20

# Function(*Integer, *Integer, *Integer => Integer)
define my_slice(source: List[Integer],
                start: *Integer = 0,
                end: *Integer = source.size()): List[Integer]
{
    return source.slice(start, end)
}

my_slice([1, 2, 3], 1)    # [2, 3]
my_slice([4, 5, 6], 0, 1) # [4]
```

The calling function runs the optional argument expressions each time they are
needed. As a result, each invocation will receive fresh versions of a default
argument that do **not** carry over into the next invocation.

```
# Function(*List[Integer] => List[Integer])
define optarg_list(x: *List[Integer] = []): List[Integer]
{
    x.push(x.size())
    return x
}

optarg_list()             # [0]
optarg_list([1, 2])       # [1, 2, 2]
optarg_list()             # [0]
optarg_list([10, 20, 30]) # [10, 20, 30, 3]
```

Mixing variable and optional arguments is permissible. By default, the vararg
parameter receives an empty `List` if no values are passed. Mixing these two
features allows a different default value:

```
# Function(Integer, *Integer, *Integer... => Integer)
define optarg_sum(a: Integer,
                  b: *Integer = 10,
                  args: *Integer... = [20, 30]): Integer
{
    var total = a + b

    for i in 0...args.size() - 1: {
        total += args[i]
    }

    print(total)
    return total
}

optarg_sum(5)              # 65
optarg_sum(5, 20)          # 75
optarg_sum(10, 20, 30, 40) # 100
```

#### Keyargs

Placing `:<name>` before the name of a parameter will allow the function to be
called using keyword arguments. Keyword arguments allow calling a function with
arguments in a different order than the function's parameters. The function can
then be called either with positional arguments or keyword arguments.

```
# Function(Integer, Integer, Integer => Integer)
define simple_keyarg(:first x: Integer,
                     :second y: Integer,
                     :third z: Integer): List[Integer]
{
    return [a, b, c]
}

simple_keyarg(1, 2, 3)                         # [1, 2, 3]

simple_keyarg(1, :second 2, :third 3)          # [1, 2, 3]

simple_keyarg(:third 30, :first 10, :second 5) # [10, 5, 30]
```

It isn't necessary to name all arguments:

```
# Function(Integer, Integer)
define tail_keyarg(x: Integer, :y y: Integer) {}

tail_keyarg(10, 20)

tail_keyarg(10, :y 20)
```

Calling a function with keyword arguments has some restrictions:

```
# simple_keyarg(:first 1, 2, 3)
# Syntax error: Positional argument after keyword argument

# simple_keyarg(1, :first 1, 2, 3)
# Syntax error: Duplicate value provided to the first argument.

# simple_keyarg(1, 2, 3, :asdf 1)
# Syntax error: 'asdf' isn't a valid keyword.
```

Keyword arguments are evaluated and contribute to type inference in the order
that they're provided:

```
var keyorder_list: List[Integer] = []

define keyorder_bump(value: Integer): Integer
{
    keyorder_list.push(value)
    return value
}

define keyorder_check(:first  x: Integer,
                      :second y: Integer,
                      :third  z: Integer): List[Integer]
{
    return keyorder_list
}

keyorder_check(:second keyorder_bump(2),
               :first  keyorder_bump(1),
               :third  keyorder_bump(3))
               # [2, 1, 3]
```

A function call with keyword arguments is verified at parse-time. The vm does
not understand keyword arguments, and the type system does not carry keyword
information either.

Despite the above, keyword arguments can be mixed together with optional
arguments and variable arguments:

```
define optkey(:x x: *Integer = 10,
              :y y: *Integer = 20): Integer
{
    return x + y
}

optkey()        # 30
optkey(50, 60)  # 110
optkey(:y 170)  # 180
optkey(4, :y 7) # 11

define varkey(:format fmt: String,
              :arg args: *String...=["a", "b", "c"]): List[String]
{
    args.unshift(fmt)
    return args
}

varkey("fmt")                # ["fmt", "a", "b", "c"]
varkey("fmt", "1", :arg "2") # ["fmt", "1", "2"]
```
