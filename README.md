#Description#
This is a ***To***y ***P***ython ***C***ompiler, heavily based on a compiler written by [Josh Wepman](https://github.com/jwepman) and myself for a compiler construction course at the University of Colorado. It compiles a subset of Python to x86 assembly.

#Future#
The compiler construction course was a trial by fire, and resulted in some messy, but functional, code. I forked off the original project, and now I'm slowly working my way through each stage, refactoring the compiler into something presentable.
Current Stage: Declassify

#Usage#
Compile source.py into asm.s (a text file containing the compiled x86 asm):

    python compile.py source.py asm.s

Enable tail call optimization:

    python compile.py -O source.py asm.s

-h for help.

#Credits#
Josh Wepman wrote at least half of the original code. 
Christopher Clark wrote the C hashtable library. 
The runtime libraries were supplied to us as part of the course.
