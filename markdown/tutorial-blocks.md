@title: Blocks

Lily's block syntax is a mixture of ideas from Python and C:

* The condition passed to a block ends with `:`

* The entire block must be enclosed in braces (instead of just the branches).

* All blocks are required to have braces.

In practice, it looks like this:

```
define did_i_pass(score: Integer, threshold: Integer): Boolean
{
    if score < threshold: {
        return false
    else:
        print("You passed!")
        return true
    }
}
```

The `:` token is used as a terminator to make the end of the block condition
unambiguous.

The style of using one brace for all branches was chosen to lessen the potential
of dangling curly braces when adjusting branch arms to support multiple
expressions.

All blocks are required to have braces to make their starting and ending points
unambiguous.

### Truthiness

Lily allows several non-`Boolean` values to be checked for truthiness. Here are
the different types and what Lily considers false for them.

| Type      | False value |
|-----------|-------------|
| `Boolean` | `false :P`  |
| `Double`  | `0.0`       |
| `Integer` | `0`         |
| `List`    | `[]`        |
| `String`  | `""`        |

### if

The most common kind of block. Unlike most curly-brace languages, branches
themselves shouldn't have braces. Instead, Lily requires the use of one set of
braces enclosing the entire if condition such as in the example above. Here's a
simple single-line set of if's.
```
define letter_for_grade(grade: Integer): String
{
    if grade >= 90:
        return "A"
    elif grade >= 80:
        return "B"
    elif grade >= 70:
        return "C"
    elif grade >= 60:
        return "D"
    else:
        return "F"
}
```

### for

Execute expression(s) while within a given range.

```
var items = ["a", "b", "c"]

for i in 0...items.size() - 1: {
    print("Item {0} is {1}.".format(i, items[i]))
}

# Result:
# Item 0 is a.
# Item 1 is b.
# Item 2 is c.
```

A `for` loop is composed of a var, start value, end value, and an increment.

If the var of a `for` loop does not exist, it is created and lasts only for the
duration of the loop. Alternatively, one can specify an existing var to use as
the counter.

The default increment is `1`. However, it is possible to specify either an
expression, or a different literal value to increment by. Note that if the loop
increment is or evaluates to `0`, an exception will be raised.

The values that a `for` loop works on (var, start, end, increment) must all be
of the type `Integer`.

```
var items = ["a", "b", "c"]

for i in items.size() - 1...0 by -1: {
    print("Item {0} is {1}.".format(i, items[i]))
}

# Result:
# Item 2 is c.
# Item 1 is b.
# Item 0 is a.
```

It is possible for the start, end, and increments to each be an expression.
Expressions are evaluated from left to right (start, end, increment), and
exactly once before the body of the loop.

```
var counter = 0

define return_counter: Integer {
    var out = counter
    counter += 1
    return out
}

for i in 0...return_counter(): {
    print("i is {0}".format(i))
}

# Result:
# i is 0
```

The control flow of a `for` loop (and other loops) can be altered by using
`continue` to jump to the top of a `for`, or `break` to exit the loop.

### while

Execute expression(s) while a predicate is truthy.

```
var i = 0
var i_values: List[Integer] = []

while i != 5: {
    i_values.push(i)
    i += 1
}

print(i_values)

# Result:
# [0, 1, 2, 3, 4]
```

For an infinite loop, use `while 1: { (expression(s)) }`. `while` supports both
`break` and `continue` for flow control.

### do

Similar to `while`, except that the body is always executed at least once:

```
var i = 1

do: {
    print(i)
} while i != 1
```

`do` supports both `break` and `continue` for flow control.

One caveat of `do` is that the condition cannot include variables declared
within the body. This restriction exists because the var's initialization may
have been skipped over by one of the above mentioned flow control keywords.

### try

Execute expression(s) while trapping for exceptions.

A `try` block attempts to execute expression(s) within the `try` section. If any
expression raises an exception, the `except` branches are tested.

```
try: {
    1 / 0
except DivisionByZeroError:
    print("Can't divide by zero.")
}
```

Similar to `if`, braces go around the entire block after the `try`'s colon:

```
try {
    1 / 0
    var v = 10
except DivisionByZeroError:
    print("Still can't divide by zero.")
}
```

Exception capture tests `except` blocks starting from the first one specified to
the last. Furthermore, capture can specify an underlying class to trap:

```
try: {
    raise ValueError("!!!")
except Exception:
    print("This will be seen.")
except ValueError:
    print("This is not possible.")
}

# Result:
# This will be seen.
```

A handful of exception classes are provided, with `Exception` being the base.
New exceptions can be created by inheriting from a predefined error class or
from `Exception` itself.

When capturing exceptions, use `as <name>` to create a var to hold the raised
exception. The var will exist until the end of the except branch on which it was
declared. The base `Exception` class provides the properties `traceback` and
`message`.

```
class MyError(message: String, var @code: Integer) < Exception(message) {}

try: {
    raise MyError("Oh no", 100)
except MyError as e:
    print("Caught custom error with code {0}, message '{1}'.".format(e.code, e.message))
}

# Result:
# Caught custom error with code 100, message 'Oh no'.
```

### match

Exhaustive selection on an enum or class.

The `match` keyword takes an expression as input, then branches off depending on
the contents. The most common use of `match` is with enums and variants. Here's
an example using the predefined `Option` with variants `Some` and `None`:

```
var v = Some("body") # Type: Option[String]

match v: {
    case Some(s):
        print("Success!")
    case None:
        print("Shouldn't reach here.")
}
# Result:
# Success!
```

This kind of matching is called `decomposition`, because the contents of the
`Option` are decomposed into vars. What makes `match` interesting is that it
requires that all cases are accounted for. If any cases are missing from a
`match` block, a syntax error is raised.

Decomposition of a variant must account for all elements. If, for example, the
`Some` case above was changed to `case Some:`, it would be an error because not
all cases are accounted for.

In some situations, one or more fields of a variant are not important. In those
situations, a single underscore ( `_` ) can be used in place of a var name to
skip decomposition:

```
enum Color {
    Red,
    Blue,
    Green,
    RGB(Integer, Integer, Integer)
}

var c = RGB(0xFF, 0xCC, 0xDD)

match c: {
    case RGB(_, blue, _):
        print("Custom color (blue: {0}).".format(blue))
    case Red:
    case Blue:
    case Green:
}

# Result:
# Custom color (blue: 204).
```

One problem with the above example is that there are three cases which don't
execute any code. One other feature of `match` is being able to use `else` to
handle all unhandled cases:

```
enum Color {
    Red,
    Blue,
    Green,
    RGB(Integer, Integer, Integer)
}

var c = Red

match c: {
    case Red:
        print("The color is red.")
    else:
}

# Result:
# The color is red.
```

The above examples all use flat enums. For custom scoped enums, `match` requires
that the variant names are qualified with their enum name. The interpreter can
infer the enum name from the type given, but requiring qualified names ensures
that scoped variants are used consistently (not scoped here, unscoped there).

`match` is also able to work against classes. Instead of the matching expression
being an enum, it is instead a class. The cases of a class match are paired up
with subclasses. This provides a safe way of testing if a value of a base class
contains an inherited class value without testing.

One caveat of `match` against classes is that, unlike `try`'s filtering, a
`case` against a base class will **not** succeed.

When matching against a class, the case must always specify a single var. That
var will have the type:

```
class MyError(message: String, var @code: Integer) < ValueError(message) { }

var v: Exception = MyError("asdf", 1234)

match v: {
    case ValueError(e):
        print("Not reachable.")
    case MyError(e):
        print("Matched to MyError with message {0} and code {1}."
              .format(e.message, e.code))
    else:
}
```

When matching to a class, the var in question must not contain generic
information, since the interpreter does not store type information at runtime,
only class information.

Another note is that in class matches, unlike enum matches, there must always be
an `else` clause present. Even if it is empty, the `else` clause serves as a
reminder that there are other potential captures to be dealt with.
