
xbin
====

A suite of Unix command line tools for englightened pipelines.


xip
---

The name "zip" was already taken.  This interlaces the contents of a
variadic list of files, especially handy with subshell file
descriptor replacement.  The following shows the opposing sides of a
six sided die.  The first example works in BSD variants, and the
second in SysV/Linux variants::

    xip <(jot 6) <(jot 6 6 1) | xargs -n 2
    xip <(seq 6) <(seq 6 -1 1) | xargs -n 2


dog
---

Buffers stdin into memory until it closes, then writes to a given
file.  This is handy for pipeline loops, where normally redirecting
to and from the same file would result in premature truncation.  The
following are equivalent::

    sort file
    cat file | sort | dog file


shuffle
-------

Shuffles the lines from standard input and writes them to standard
output.  If the input stream is indefinite, the input can be
shuffled indefinitely by specifying a pool size as a second
argument.



enquote
-------

Enquotes every line from standard input and writes it to standard
output.  Handy for pipelines that end in xargs, when file -print0
and xargs -0 aren't really an option.  The following are pretty
close to equivalent:

    find . -print0 | xargs -0 tar cf -
    find . | enquote | xargs tar cf -
    

cycle
-----

Reads all of standard input and writes it back, repeatedly, to
standard output.  The first pass gets written immediately, so an
indifinite stream will only cause memory bloat at the rate at which
cycle's standard output is consumed::

    find . -name '*.mp3' \
    | cycle \
    | shuffle 10000 \
    | enquote \
    | xargs -n 1 mpg123


findall
-------

Convenience command for find . -name "<file_pattern>" -print0 | xargs -0 grep "<grep_pattern>". Significantly faster than grep -r.

    findall "<pattern1>"

is equivalent to

    find . -name "*" -print0 | xargs -0 grep "<pattern1>"

while

    findall "<pattern1>" "<pattern2>"

expands to

    find . -name "<pattern1>" -print0 | xargs -0 grep "<pattern2>"


samp
----

Writes a random sample of the lines from standard input back out to
standard output.  Specify a sample size as an argument.  The sample
is in stable order.  The input stream may safely be of indefinite
size.

This program is called `samp` so as not to collide with bsd's `random`
or OS X's `sample`.


unique
------

Reads lines from standard input and writes the first of each unique
line.  This is similar to the behavior of the highly optimized `uniq`.
`uniq` suppresses the output of sequentially redundant lines, so to
create a truly unique set, the common idiom is to sort the input.
However, this does not preserve the order.  In this sense, `unique` is
a "stable" operation.

The following are equivalent:

    cat input | sort | uniq | dog output
    cat input | unique | sort | dog output

Example, removing redundant elements from `$PATH`:

    export PATH=$(
        echo $PATH \
        | tr ':' '\n' \
        | unique \
        | paste -sd: -
    )

