#!/usr/bin/env python
# this tool is generally available on Linux,
# but not BSD or Mac OS X.
import sys
for line in reversed(sys.stdin.readlines()):
    print line,
