@title: Welcome
Lily is a programming language that's been under development for
several years. Lily is **statically-typed**, with an interpreter as a reference.
Lily uses **reference counting** for memory management with **garbage
collection** as a fallback.

Key features of Lily:

* Built-in template mode
* Embed/extend in C
* Single-inheritance classes
* Exceptions
* Generics
* Abstract data types (with `Option` and `Result` predefined).

Here's a small example showing most of Lily's features:

```
var math_ops = ["+" => (|a: Integer, b: Integer| a + b),
                "-" => (|a, b| a - b),
                "*" => (|a, b| a * b),
                "/" => (|a, b| a / b)]

define rpn(input: String): Result[String, List[Integer]]
{
    var values = input.split(" ").reject(|r| r.is_space() )
    var stack: List[Integer] = []

    for i in 0...values.size() - 1: {
        var v = values[i]
        match v.parse_i(): {
            case Some(number):
                stack.push(number)
            case None:
                if stack.size() < 2:
                    return Failure("Stack underflow.")

                var right = stack.pop()
                var left = stack.pop()
                try: {
                    var op_fn = math_ops[v]
                    var op_value = op_fn(left, right)
                    stack.push(op_value)
                except KeyError:
                    return Failure("Invalid operation {0}.".format(v))
                except DivisionByZeroError:
                    return Failure("Attempt to divide by zero.")
                }
        }
    }

    return Success(stack)
}

var lines = [
    "1 2 3 4 * + -",
    "2 2 2 2 * *",
    "*",
    "1 2 ?"
    ]

lines.each(|l| print("{0}: {1}".format(l, rpn(l)) ) )

# Result:
# 1 2 3 4 * + -: Success([-13])
# 2 2 2 2 * *: Success([2, 8])
# *: Failure("Stack underflow.")
# 1 2 ?: Failure("Invalid operation ?.")
```
