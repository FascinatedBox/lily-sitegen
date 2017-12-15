@title: Exceptions

Occasionally there are errors that are not expected: A subscript of a `List` is
out-of-bounds or there is an accidental attempt to divide by zero. In many
cases, the use of `Option` or `Result` is preferable to using an exception. Lily
has predefined exceptions for when those enums are not suitable.

The base of all exceptions is the `Exception` class. It is predefined as
follows:

```
class Exception(var @message: String) {
    public var @traceback: List[String] = []
}
```

When an exception is raised, the `traceback` field of it is replaced with the
current call stack.

### Hierarchy

The exception hierarchy is as follows:

* `DivisionByZero`: Attempt to divide or modulo by zero.

* `Exception`: Base class of all raiseable exceptions.

* `IndexError`: Out-of-bounds access of a container (such as `List`).

* `IOError`: Incorrect usage of a `File`.

* `KeyError`: Attempt to read a value from a `Hash` that does not exist.

* `RuntimeError`: Bad runtime action such as modifying a hash during iteration
                  or exceeding the recursion limit.

* `ValueError`: Invalid or unreasonable value provided.

Any of these exceptions can be inherited to create a custom exception. The try
section in the blocks area details how `try/except` works, and more on raising
custom exceptions.

