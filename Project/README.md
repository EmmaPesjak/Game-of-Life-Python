# Project
Emma Pesjak 2021-10-XX
## Environment & Tools
The laboration was performed on a Windows 10 PC with PyCharm 2021.2.1, Python 3.9.7 and Git version 2.33.0.windows.2. 
The sources of information used for this laboration has been course literature
(chapters 4-9, 12 in Python Basics, fourth edition), course material from modules 1-6,
!!
and a webpage on string formatting from [Stackabuse](https://stackabuse.com/formatting-strings-with-python/) 
accessed 2021-09-30.
!!


https://www.youtube.com/watch?v=9bFvpOFyClI accessed 2021-10-13
https://stackoverflow.com/questions/18938276/how-to-convert-nested-list-of-lists-into-a-list-of-tuples-in-python-3-3  accessed 2021-10-13

https://www.youtube.com/watch?v=-ARI4Cz-awo accessed 2021-10-14
https://www.youtube.com/watch?v=jxmzY9soFXg accessed 2021-10-14
https://www.youtube.com/watch?v=FsAPt_9Bf3U accessed 2021-10-14


## Purpose
The purpose of this project has been to demonstrate my new programming skills and understanding of all the learning
modules of this course. Functions, logging, decorators, json-files, file handling etc.

## Procedures

## Discussion





parse_world_size_arg
had trouble with wrong error message when empty string from .split
assert was hard to grasp since it is "backwards thinking".

completed the base implementations 
populate_world

calc_neighbour_positions
this was the most straigt forward function, basically nothing hard, just make a list of tuples of neighbours
am aware that it could be done in one line but thought it was better to list all  N, NW, E, SE.... for readability


run_simulation
also pretty straight forward

update_world
None cells easy fix
tricky to get the neighbours count right for next gen
här är det ju lite fult att jag först sätter alla till alive och sen delar in dem av ålder.


count_alive_neighbours


grade d recursive
did not know you could return (void) this caused a hick-up

grade c load seed from file
pretty straight forward to implement but getting the population dictionary correct was a bit of a challenge.



furthermore...


eventuellt se om jag kan göra några if/else till oneliners
eventuellt fixa grannarna utan att göra variabler (N, NW, NE.....)