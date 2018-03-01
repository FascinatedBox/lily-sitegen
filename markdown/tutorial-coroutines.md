@title: Coroutines

A typical `Function` runs and returns a single value at the end of execution.
The main feature of a `Coroutine` is that it can yield values at different
points along its execution. Another advantage of a `Coroutine` is that it has an
execution stack that belongs to it.

### Creation

The simplest kind of `Coroutine` yields `Integer`, doesn't need any messages,
and doesn't take extra arguments:

```
define one_to_ten(co: Coroutine[Integer, Unit])
{
    for i in 1...10:
        co.yield(i)
}

var co = Coroutine.build(one_to_ten)

co.resume() |> print # Some(1)
co.resume() |> print # Some(2)
co.resume() |> print # Some(3)
co.resume() |> print # Some(4)
co.resume() |> print # Some(5)
co.resume() |> print # Some(6)
co.resume() |> print # Some(7)
co.resume() |> print # Some(8)
co.resume() |> print # Some(9)
co.resume() |> print # Some(9)
co.resume() |> print # Some(10)
co.resume() |> print # None
```

For a `Function` to be eligible to be the base of a `Coroutine`, it needs to
take a `Coroutine` value as a first parameter. This allows Lily to make sure
that only the proper type of a value is yielded back. Another advantage to this
design is that there are no new keywords imposed by supporting coroutines.

The type of the `Coroutine` tells what it is able to do. The first type is what
type it can yield, and the second is what kind of type it can be resumed with.
In the above example, the `Coroutine` doesn't need to be resumed with any value,
so the resumption type is `Unit` and `Coroutine.resume` is used.

Since yield requires the currently-running `Coroutine`, functions called by the
base of a coroutine cannot yield unless they have that value. It is therefore
possible to use the type system to determine what functions may yield, and what
ones may not.

Because of how coroutine values are initialized, they can be chained:

```
define count_three_times(co: Coroutine[Integer, Unit])
{
    one_to_ten(co)
    one_to_ten(co)
    one_to_ten(co)
}
```

The above function works regardless of if `count_three_times` is sent to
`Coroutine.build`, or was called from some other coroutine. What matters is
that they have the same contract (same yield type, same message type).

### Caveats

Exceptions stay within their originating coroutine:

```
define error(co: Coroutine[Integer, Unit])
{
    co.yield(0 / 0)
}

Coroutine.build(error).resume() |> print # None
```

Returns from the base `Function` are ignored:

```
define noop(co: Coroutine[Integer, Unit]): Integer { return 10 }

Coroutine.build(noop).resume() |> print # None
```

`Coroutine.yield` requires the coroutine value that is currently running.

`Coroutine.yield` works through any number of native calls, but not through a
foreign call. Typical examples are 'select', 'map', etc. Attempting to yield
while in a foreign call will result in the resumer getting `None` since an
exception is raised.

```
define invalid_yield_each(co: Coroutine[Integer, Unit])
{
    [1, 2, 3].each(|e|
        co.yield(e)
    )
}

Coroutine.build(invalid_yield_each).resume() |> print # None
```

`Coroutine.receive` only works when the source coroutine is the currently
executing one (not just executing, but also the current one).

### States

A `Coroutine` can be in one of exactly four different states:

* `done`: The base function is done.

* `failed`: An exception was raised.

* `waiting`: Waiting to be resumed.

* `running`: Currently executing code.

Note that a coroutine can be running, but not be the currently running
coroutine, such as in a case where 2 or more are currently be resumed.

### Arguments

Sometimes there's a reason for a coroutine to take another value:

```
define yield_list(co: Coroutine[Integer, Unit], source: List[Integer])
{
    for i in 0...source.size() - 1:
        source[i] |> co.yield
}

var co = Coroutine.build_with_value(yield_list, [1, 2, 3])

co.resume() |> print # Some(1)
co.resume() |> print # Some(2)
co.resume() |> print # Some(3)
co.resume() |> print # None
```

`Coroutine.build_with_value` allows sending in an extra argument. If 2+
arguments are needed, consider sending a `Tuple` (and having the caller unpack
it).

```
define range(co: Coroutine[Integer, Unit], start_end: Tuple[Integer, Integer])
{
    var start = start_end[0]
    var end = start_end[1]

    if start < end:
        for i in start...end:
            co.yield(i)
}

var co = Coroutine.build(range, <[1, 3]>)

co.resume() |> print # Some(1)
co.resume() |> print # Some(2)
co.resume() |> print # Some(3)
```

Alternatively, the caller may want to use a closure:

```
define range_cl(:start start: Integer,
                :end end: Integer)
{
    define range_fn(co: Coroutine[Integer, Unit]) {
        if start < end:
            for i in start...end:
                co.yield(i)
    }

    return range_fn
}

var co = range_cl(:start 1, :end 3) |> Coroutine.create

co.resume() |> print # Some(1)
co.resume() |> print # Some(2)
co.resume() |> print # Some(3)
co.resume() |> print # None
```

### Messages

It's possible to have a coroutine that receives messages in addition to yielding
values:

```
define adder(co: Coroutine[Integer, Integer], source: List[Integer])
{
    for i in 0...source.size() - 1:
        co.yield(co.receive() + source[i])
}

var co = Coroutine.build_with_value(adder, [1, 2, 3])

co.resume_with(10) |> print # Some(11)
co.resume_with(200) |> print # Some(202)
co.resume_with(3003) |> print # Some(3003)
```

A coroutine eligible for messages (second type being non-`Unit`) is resumed with
`Coroutine.resume_with`, and must pass a value each time.

On the other end, the coroutine can fetch the value it was sent using
`Coroutine.receive`. Receiving a value does not consume it or alter it, so a
coroutine is permitted to call receive as many times as it wishes.
