@title: Generics

In Lily, classes, enums, and functions can make use of generics. Currently,
generics are quite limited:

They must be a single capital letter, must be declared before use, and there are
no traits or qualifiers.

All of those issues will be addressed in a future version of the language. Even
with those restrictions, generics are quite useful.

```
define transform[A, B](input: A, fn: Function(A => B)): B
{
    return input |> fn
}

transform("10", String.parse_i) # Some(10)

define ascending(a: Integer, b: Integer): Boolean { return a > b }
define descending(a: Integer, b: Integer): Boolean { return a < b }

define sort_inplace[A](lst: List[A], cmp: Function(A, A => Boolean)): List[A]
{
    for i in 0...input.size() - 1: {
        var j = i
        while j > 0 &amp;&amp; cmp(input[j - 1], input[j]): {
            var temp = input[j]
            input[j] = input[j - 1]
            input[j - 1] = temp
            j -= 1
        }
    }
    return input
}

sort_inplace([1, 3, 5, 2, 4], ascending)  # [1, 2, 3, 4, 5]
sort_inplace([1, 3, 2],       descending) # [3, 2, 1]

class Container[A](input: A) {
    public var @contents = [input]

    public define push(value: A): self {
        @contents.push(value)
    }
}

var v = Container(1)
        .push(2)
        .push(3)

print(v) # [1, 2, 3]
```
