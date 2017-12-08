lily-sitegen
============

This repository contains the scripts, templates, and markdown used to build
Lily's website. It's organized as follows:

* gen_basic: Turns markdown files into equivalent html files. Each markdown file
             starts with `@title: <x>` that becomes the html file's title.

* gen_core: Uses a modified lily-parsekit/docgen to generate documentation from
            lily's lily_pkg_core.c. Requires lily-mkdir (both under
            `FascinatedBox`).

* gen_sandbox: Generates the sandbox html by html escaping some examples. The
               sandbox js is not updated, however.

Use `sitegen.py` with a path to lily's `lily_pkg_core.c` to generate output into
a directory named `output`.
