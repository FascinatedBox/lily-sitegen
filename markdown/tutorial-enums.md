@title: Enums

Enums are a datatype composed of a fixed set of variant classes. A variant class
can take any number of types (including the enum itself), or can be empty. Enums
declarations can include methods as well as variants.

```
enum Rgb {
    Red,
    Green,
    Blue

    define is_blue: Boolean {
        match self: {
            case Blue: return true
            else:      return false
        }
    }
}

var v = Blue

print(v.is_blue()) # true
print(v) # Blue
```

Since enums aren't inheritable, their methods don't need qualifiers like with
user-defined classes.

By default, variants of an enum are flat. Variants of a flat enum can be
referenced directly.

In contrast, the `scoped` qualifier makes it so that variants of an enum are
only accessible through the enum name:

### Scoped enums

```
scoped enum Rgb {
    Red,
    Green,
    Blue

    define is_blue: Boolean {
        match self: {
            case Rgb.Blue: return true
            else:          return false
        }
    }
}

var v = Rgb.Blue

print(v.is_blue()) # true
print(v) # Rgb.Blue
```

### Varargs

Variants can be declared to take varargs. If they do, the extra arguments (if
any are given) are put into a `List`.

```
enum Example {
    ManyInts(Integer...),
    Nothing
}

var v = ManyInts(1, 2, 3, 4)

match v: {
    case ManyInts(m):
        print(m)
    else:
}

# Result:
# [1, 2, 3, 4]
```

### Optargs

Variants are not able to use optional arguments, because they are not actually
functions.

### Keyargs

Variants can hold keyword arguments:

```
scoped enum Item {
    Thing(:left Integer, :right Integer)
    Other
}

var v = Item.Thing(:left 1, :right 2)

v = Item.Thing(1, 2)
```
