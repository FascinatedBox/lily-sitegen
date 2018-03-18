@title: Basics

### Declarations

Variables must be declared before they are used, with the `var` keyword:

```
var a_number = 10
var my_double = 5.55, some_string = "Hello"
var number_list = [1, 2, 3]
```

The value used to initialize a var determines the type of the var. In most
cases, `var` does not need extra type information. However, sometimes the right
side of an initialization doesn't provide enough info and type information must
be provided:

```
var string_list: List[String] = []
```

### Literals

Lily comes with several predefined classes, and syntax for using them as well.

#### Boolean

Either `true` or `false`.

#### Byte

A numeric value from 0 to 255 (inclusive). Can be declared like an `Integer` but
with a suffix of `t`, or like a `String` using a single character or escape
sequence between single quote marks:

```
0t
0xFFt
255t
'a'
'\t'
```

#### ByteString

An array of `Byte` values. A `String`, but with no guarantees about embedded
`\0` values or utf-8. Allows any escape character between quotes:

```
B"123456"
B"\0\1\2"
B"\255\254\t"
B"""A \
    multi-line \
    ByteString"""
```

The backslash-newline escape sequence lets the interpreter know to omit the
newline of the current line and the leading whitespace (spaces and tabs) of the
next line.

#### Double

Represents either very large or very small values:

```
0.00000005
-1.7
10e1
5e-5
```

#### Hash

A `Hash` is a key to value mapping. Only `Integer` and `String` can be used for
the key. The value can be anything, so long as there is a consistent type. If a
`Hash` literal contains the same key twice, both values will still be computed
if necessary, but the right-most key 'wins':

```
var string_to_integer_map = ["abc" => 1, "def" => 2, "ghi" = 3]

var empty_string_double_hash: Hash[String, Double] = []
```

#### Integer

A 64-bit signed value that can be represented using different bases:

```
12345
-67890
0c744
x0xFF
0b101010101
```

#### List

A `List` is composed of values put together in brackets. The values must have
some common underlying type:

```
var integer_list = [1, 2, 3]

var empty_boolean_list: List[Boolean] = []
```

#### String

Represents a block of text. `String` carries the guarantee that all instances
are valid utf-8, and that they do not carry `\0` characters inside. `String`
literals are single-line by default, but can be multi-line as well:

```
var message = "Hello"

var multi_line = """Hello \
                    there"""
```

The backslash-newline escape sequence lets the interpreter know to omit the
newline of the current line and the leading whitespace (spaces and tabs) of the
next line.

#### Tuple

A `Tuple` is similar to a `List`, except that `Tuple`s have a fixed size, but
can types that don't have any similarity to each other. A `Tuple` begins with
`<[` and ends with `]>`:

```
var record = <[1, "abc", [2]]>

var t: Tuple[String, Integer] = <["asdf", 123]>
```

### Keywords

The following keywords have special meaning:

```
break case class continue define do elif else enum except false __file__ for
forward __function__ if import __line__ match private protected public raise
return scoped self static true try unit var while
```

Some of these keywords are 'magic', in that they are replaced with a literal
when they are used:

* `__file__`: The path to the current file.
* `__line__`: The current line number.
* `__function__`: The name of the current function.

### Comments

Lily supports two kinds of comments:

```
# This is a single-line comment

#[ This
   is
   a
   block
   comment ]#
```

### Escape Codes

`String`, `ByteString`, and `Byte` support the following escape sequences:

* `\a`: Terminal bell

* `\b`: Terminal backspace

* `\t`: Tab

* `\n`: A newline

* `\r`: Carriage return

* `\"`: The `"` character

* `\'`: The `'` character

* `\\`: The `\` character

* `\/`: `\` on Windows, `/` elsewhere.

* `\nnn`: 'nnn' is up to 3 digits, scanned in decimal. This can yield any value
           between 0 and 255 inclusive. Scanning stops either after 3 digits
           have been consumed, or a non-base 10 digit occurs.

* `\<newline>`: `ByteString` and `String` only. The newline of the current line
                and the leading whitespace (`' '` or `'\t'`) will be omitted
                from the literal.

### Precedence

Lily's precedence table, from lowest to highest:

| Operator                | Description              |
|-------------------------|--------------------------|
| `= /= *= += -= <<= >>=` | Assign/compound assign   |
| `||`                    | Logical or               |
| `&&`                    | Logical and              |
| `>= > < <= == !=`       | Comparison and equality  |
| `++`                    | Concatenate              |
| `|>`                    | Function pipe            |
| `& | ^`                 | Bitwise and, or, xor     |
| `<< >>`                 | Bitwise shifts           |
| `+ -`                   | Plus, minus              |
| `% * /`                 | Modulo, multiply, divide |

Operations such as `x.y` member lookup and subscripts take over either the
entire current value, or the right side of the current binary operation.

### Operations

Basic arithmatic operations (`+ - * /`) can be used for two `Double` values, or
two `Integer` values, or when there is one `Double` and one `Integer` value. The
result is a `Double` if either side is a `Double`, `Integer` otherwise.

Other primitive operations (shifts, bitwise operations, and modulo) are only
valid if both sides are `Integer`.

Comparison operations (`>= > < <=`) are allowed on any two sets of `Integer`,
`String`, or `Double`.

### Comparison

Equality operations (`== !=`) are allowed on any two equivalent types.

Simple values like `Integer`, and `Double` are straightforward: They are equal
only when they are the same value.

`List`, `Tuple`, `Hash`, and variants use structural comparison. Since `List`
uses structural comparison, `[1] == [1]` will always return `true`.

All other containers and more interesting types use identity comparison.
A comparison such as `Point2D(2, 4) == Point2D(2, 4)` will always return
`false`, since each `Point2D` is a different instance.

### Interpolation

The `++` operator, `String.format`, and `print` all make use of built-in
interpolation. Interpolation works as follows:

Primitive values such as `Integer`, `Double`, and `String` have their content
written out.

Built-in containers have their inner contents written out. `Hash` does not
guarantee an ordering to the contents it writes out.

Non-scoped variants print just their name and their contents. Scoped variants
print out the enum name and a dot first.

Classes ( `Dynamic` included ) print out their address.
