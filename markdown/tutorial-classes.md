@title: Classes

User-declared classes provide a way to group together a set of data and related
functions. In Lily, classes are only allowed to have one parent class at most as
a way of keeping their internal implementation simpler.

A simple class declaration of a 2d point (x and y coordinate) looks like this:

### Declaration

```
class Point(x: Integer, y: Integer) {
    public var @x = x
    public var @y = y
}
```

In Lily, the body of the `class` block serves to both define class variables and
to initialize them.

Inside a class, properties have a `@` prefix like in Ruby. Outside of it, both
methods and properties are accessed using a dot.

```
class Point(x: Integer, y: Integer) {
    public var @x = x
    public var @y = y

    public define increase(x_value: Integer, y_value: Integer) {
        @x += x_value
        @y += y_value
    }
}

var p = Point(5, 10)

print(p.x) # 5

p.increase(100, 200)

print(p.y) # 210
```

In situations like the above where the inputs to a class become public class
properties, a shorthand is available:

```
class Point(var @x: Integer, var @y: Integer) {  }
```

Since both class properties and class methods are accessed the same outside of a
class, it is a syntax error to have a property and a method with the same name.

### Scope

Prior to declaring a class member, a scope is needed. There are three possible
scopes that a class member or function can have:

`public` denotes that the member is available anywhere.

`protected` restricts the member to the class itself, or any class that inherits
from it.

`private` restricts the member to only the class.

### Inheritance

Classes use the `<` token to denote inheriting from another class when writing
the header:

```
class Point2D(var @x: Integer, var @y: Integer) {}

class Point3D(x: Integer, y: Integer, var @z: Integer) < Point2D(x, y) {}
```

But what about chaining methods from different classes? Lily allows using a
return type of `self` as a special case for class methods. This special case
allows chaining methods without losing type information:

```
class Point2D(var @x: Integer, var @y: Integer) {
    public define increase_xy(x_value: Integer, y_value: Integer): self {
        @x += x_value
        @y += y_value
    }
}

class Point3D(x: Integer, y: Integer, var @z: Integer) < Point2D(x, y) {
    public define increase_z(z_value: Integer): self {
        @z += z_value
    }
}

var p3d = Point3D(10, 20, 30)

p3d.increase_xy(100, 200)
   .increase_z(300)

var result = [p3d.x, p3d.y, p3d.z]

print(result)

# Result:
# [110, 220, 330]
```

### static

By default, class methods receive an implicit `self` parameter as their first
argument. The `static` qualifier, when applied to a class method, turns that
behavior off:

```
class Utils {
    public static define square(x: Integer) { return x * x }
}

var v = Utils.square(10) # 100
```
