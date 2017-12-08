@title: Install

### Requirements

To use Lily on your local machine, you'll first need to build it. Building the
interpreter can be done in a few commands. You'll need two tools first:

* cmake, at version 3.0.0 or better
* A modern C (C11) compiler. MSVC, gcc, and clang are known to work.

### Install

Grab the Lily source code through whatever means you'd like. Open up a
command-line prompt in the Lily directory and issue the following:

```
cmake .
make
make install
```

The result of the above is an executable named `lily` and a library that your
programs can link to named `liblily`. 

### Options

The following configuration options can be passed to `cmake` to alter the build:

`-DWITH_SANDBOX=(on|off)`: Defaults to `off`. If this is set to `on`, then the
website sandbox will be built. This option requires `emscripten` to exist and be
loaded in the current environment. An error is printed if either is lacking.

### Usage

Create a file called `hello.lily` and save the following to it:

```
print("Hello, world!")
```

Execute the script with a console using `lily hello.lily`. You should see the
message show up on your console.

It's also possible to invoke the interpreter entirely from the console:

```
lily -s 'print("Hello, world!")`
```

By default, scripts are read in code-only mode. In this mode, all input is fed
to the interpreter is read and executed. The alternative is template mode,
wherein code is between `<?lily ... ?>` tags. Create another file called
`template_hello.lily` with the following:

```
<?lily ?>
<html>
    <body>
        <?lily print("<p>Hello World</p>") ?>
    </body>
</html>
```

Execute the script from the console using `lily -t template_hello.lily`. This
time, the output will be just the html. By using the `-t` switch, the executable
invokes the interpreter in template mode.

In template mode, input to the interpreter is treated as content first. Only
what's between `<?lily ... ?>` tags is executed as code. Template mode files
require a tag at the very start of input. That prevents code-mode files from
being passed to template mode.

Finally, regardless of the mode that the interpreter starts in, subsequent
imports always load in code-only mode. Combined with the tag restriction, it's
possible to safely use code-mode libraries in template-mode modules.
