@title: Bindgen

Usage: `lily bindgen.lily <some c file>`

Bindgen is a tool for helping extend the Lily interpreter with new classes,
enums, methods, and so on. This tool generates bindings for the interpreter to
load what you've made. Before you begin, you should be familiar with writing
Lily code, and also comfortable with C as well.

Bindgen is in the `FascinatedBox/lily-parsekit` repo at Github.

## Why this tool exists

Most interpreters are extended by having the C library export a special function
that they will look for. That function then calls back into the interpreter to
add functions, classes, and so forth. For those, no binding tool is necessary.

Lily's loading mechanism is different, consisting of a string table holding
definitions, and a loading function. The loading function returns C function
pointer or, in the case of vars, provides the interpreter to the var loader so
the var loader can push relevant information back.

Since Lily is statically-typed, the overhead required for storing definitions,
classes, and enums is greater because of the typing involved. Furthermore, a
user is loading a large library, there is a chance that they may not need all of
what the library exports. In the reverse, where all elements of a library are
used, the cost of several table lookups should be negligible compared to the
time used processing the entire program.

The interpreter uses this lazy loading system (termed dynaload in much of Lily)
as a means of saving both memory and time by avoiding loading the over 70
functions in the builtin library unless the type system can prove they are
needed.

## How this tool works

This tool works by reading in a source `.c` file. It will look for comments that
follow this form:

```
/**
thing blah blah

information about the thing
*/
```

The tool treats 'thing' as a command. Everything from that until the first blank
line is data the command. What proceeds after the blank line is treated as
documentation for 'thing'. From these comments, the tool will build macros, a
table, and a loader for you.

The contents generated by the tool are placed in the autogen section of the
file. The autogen section of the file is denoted by the following:

```
/** Begin autogen section. **/
/** End autogen section. **/
```

In terms of organization, the first command should be the `library` command that
specifies the name of what you're creating, and the library's documentation.
After that should be classes and enums. Finally, package-level vars and
functions should be last.

## Issues

* Classes must be mentioned before their use.
* Modules cannot export sub modules (may not happen).
* The tool allows a 'static' qualifer, but the language does not (yet).
* Foreign classes cannot be marked by the garbage collector.
* Enums are undocumented since they don't work externally yet.

## Commands

The rest of this document focuses on commands that are available, what they
generate, and sometimes how to use it.

Some keywords create a scope. The `define` keyword will create definitions under
the current scope as long as the name has the scope as a qualifer. For example,
writing `File.print` instead of just `print`.

A scope is complete when another scope begins or when an unqualified define is
seen.

### library <name>

This command specifies the name of the package. This is used later by `var` and
`define` for locating functions:

Given the library name `builtin`:

* Method `to_s` in `Integer`: `lily_builtin_to_s`.

* Constructor for `Exception`: `lily_builtin_Exception_new`.

* Toplevel function `calltrace`: `lily_builtin__calltrace`.

* Toplevel var `stdout`: `lily_builtin_var_stdout`.

* A teardown function for `File`: `destroy_File`.

### native class <name> <ctor> (< parent)? '{' <properties> ... '}'

This introduces a native class to the interpreter. A native class can inherit
another native class, as well as be inherited. The `<ctor>` section is processed
as arguments that will need to be passed to invoke the `<name>(...)` class
constructor.

Normally, Lily will reject a definition that has an empty `()`. However, both
`native class` and `foreign class` allow for empty `()` for a constructor that
does not take arguments.

Make sure to not put a blank line in the property section, or the tool will
assume the contents following it are a documentation comment. Be aware that the
interpreter won't call underlying constructor functions either, as it assumes
the foreign constructor will do it.

An an example, here is the definition for `Exception`:

```
native class Exception {
    var @message: String
    var @traceback: List[String]
}
```

Since neither property has a `protected` or `private` qualifier, both are
publically accessible. As for initialization, it works as follows:

```
void lily_builtin_Exception_new(lily_state *s)
{
    lily_container_val *result = lily_push_super(s, id, 2);

    lily_con_set(result, 0, lily_arg_value(s, 0));

    lily_push_list(s, 0);
    lily_con_set_from_stack(s, result, 1);
    lily_return_super(s);
}
```

The function `lily_push_super` will check to see if an in-progress class has
been passed. It will return either that, or a newly-made instance. From there,
the message (0) and traceback (1) fields are set.

### foreign class <name> <ctor>? '{' <layout> '}'

This introduces a foreign class to Lily. Foreign classes are implemented as a
wrapper class, to which you can add members that you wish. Here is an example
from the `postgres` wrapper library:

```
/**
foreign class Conn {
    layout {
        uint64_t is_open;
        PGconn *conn;
    }
}

The `Conn` class represents a connection to a postgres server.
*/
```

The tool will generate a `lily_postgres_Conn` struct in the header section as
well as an init macro so that Lily can allocate memory for one of the structs.
One example of initializing the given struct:

```
    PGconn *conn = PQsetdbLogin(...);

    if (PQstatus(conn) == CONNECTION_OK) {
        lily_postgres_Conn *c = INIT_Conn(state)
        c->is_open = 1;
        c->conn = conn;
        lily_return_top(state, (lily_foreign_val *)c);
    }
    else {
        /* error handling */
    }
```

The `INIT_<class>` macro generated expects a destroy function that must be
written. The destroy function can be run directly from a deref step of the
interpreter, or as a side-effect of garbage collection. The destroy function is
provided with a value, and is responsible for cleaning out what was not created
by the interpreter.

```
void destroy_Conn(lily_postgres_Conn *conn_value)
{
    PQfinish(conn_value->conn);
}
```

The interpreter is written with the intention that value teardown does not
produce side-effects such as changing other values or execute code. It is
assumed that foreign function teardown will honor that.

### define <name> <type>

This makes `<name>` available with the type provided. The type is allowed to
directly access package classes and builtin classes as if you were writing the
definition in Lily. 

If the definition is part of a class, it is automatically assumed to be public.
If that is not wanted, then `protected` or `private` can be added before
`define`. The tool will also automatically insert `self` as the first argument
to a method. The `static` qualifier will instruct the tool to not do that.

Although a `define` type may mention optional arguments, be aware that the
interpreter will not implement them. Instead, it is the responsibility of the
definition implemenation to implement optional arguments. Here's an example of
how to do so:

```
/**
define add(a: Integer, b: *Integer=10): Integer

Add two numbers together, or use '10' if the second number isn't given.
*/
void lily_math__add(lily_state *s)
{
    int left = lily_arg_integer(s, 0);
    int right;

    if (lily_arg_count(s) == 2)
        right = lily_arg_integer(s, 1);
    else
        right = 10;

    lily_return_integer(s, left + right);
}
```

### var <name> ':' <type>

This makes `<name>` available to the interpreter. Var loading is done by having
a var loading function push a value onto the interpreter. Var loaders must begin
with `load_var_` as a prefix. A var loader can push a value as simple or as
complex as they wish. A var loader should never have side-effects such as
executing code or relying on global data. Here's an example that exports
apache's request method as `server.http_method`.

```
/**
var http_method: String

This is the method that was used to make the request to the server.
Common values are "GET", and "POST".
*/
static void load_var_http_method(lily_state *s)
{
    request_rec *r = (request_rec *)lily_config_get(s)->data;

    lily_push_string(s, r->method);
}
```