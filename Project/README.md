# Project
Emma Pesjak 2021-10-XX

## Environment & Tools
The project was performed on a Windows 10 PC with PyCharm 2021.2.1, Python 3.9.7 and Git version 2.33.0.windows.2. 
The sources of information used for this project has been course literature
(chapters 4-9, 12 in Python Basics, fourth edition), course material from modules 1-6, a webpage on 
nested lists of tuples from
[Stackoverflow](https://stackoverflow.com/questions/18938276/how-to-convert-nested-list-of-lists-into-a-list-of-tuples-in-python-3-3) 
accessed 2021-10-13, [this video](https://www.youtube.com/watch?v=9bFvpOFyClI) by Soumil Shah accessed 2021-10-13,
and videos [1](https://www.youtube.com/watch?v=-ARI4Cz-awo), [2](https://www.youtube.com/watch?v=jxmzY9soFXg),
[3](https://www.youtube.com/watch?v=FsAPt_9Bf3U) by Corey Schafer accessed 2021-10-14.


## Purpose
The purpose of this project has been to demonstrate my understanding of what this course's learning modules 
has aimed to teach, for example data types, functions, logging, decorators, json-files and file handling.


## Procedures
First, the base implementations for grade E was completed, beginning with the `parse_world_size_arg` function. 
The user input was a string with the format width x height. And the function needed to convert this into integers in 
a tuple. By splitting the string input at the "x" with the `.split()` function into a width_height variable, 
values for width and height could be extracted. But first in a `try` block, with an `assert-statement` 
the user input was validated with the help of the `len()` function to see that the user had not written too few 
or too many values, it had to be for example 80x40. Width and height were extracted from the width_height 
variable and converted to integers with the `int()` function. With an `if-statement` a ValueError would be raised 
if either height or width were below one. With an `except`, if the user input was for any reason incorrect the program 
would write the `assertion` or error message in the console and use the default value of 80x40.

The next step was to complete the `populate_world` function which created the initial population of cells.
An empty population dictionary was created to be later filled in. The `get_pattern` function from the code base was 
called and stored in the variable pattern, in case of that the user would use a seed pattern, the function returned
None if no pattern was to be used. Width and height coordinates were extracted from the world size tuple input, 
and to get every coordinate the `range()` function was used. With `itertools product()` the coordinates were matched 
together for each row and column. Then a `for-loop` that iterated over the coordinates was done. 
In order to conform with the provided seed patterns in the code base, the axes of the coordinates were flipped 
to (y, x). Another cell dictionary was created since the population dictionary had the coordinates as keys and 
the cell dictionary as values, the cell dictionary contained the cells states and neighbours 
(and later also age for the grade A implementation). The edge of the world, to define the border consisted 
of rim-cells, a special type of cell that instead of a cell dictionary had the value of None. The rim-cells were 
declared with an `if-statement` which stored the rim-cells in the population dictionary, the rim-cells will always 
have either a 0 in the coordinates or the coordinate of the width or length minus one. To make sure that the rim-cells 
would not get a cell state, a `continue` was put in the `if-statement` to continue to the next cell coordinates. 
The rest of the cells states were then declared. With another `if-statement` the cells were set to alive or dead by 
comparing coordinates with the coordinates in the pattern variable in case of if the user used a seed pattern. The
`else` then would randomize the cell states if no pattern were to be used. A randomization from 0-20 was done by 
using the `randint()` function from the random module. A value above 16 would set the cell as alive and a value of 
16 or below would set the cell as dead. Lastly the cell states and neighbours were mapped to the cell dictionary, 
the neighbours by calling the `calc_neighbour_positions` function, and the cell dictionary was mapped to the 
coordinated in the population dictionary.

The `calc_neighbour_positions` function was then completed simply by getting the coordinates from the 
input "_cell_coord" and putting these into the variables y and x. This might seem backwards but the axes were flipped 
in order to conform with the provided seed patterns in the code base. The function then returned a list of tuples
with the neighbours coordinates calculated by offsetting their positions in all directions (north, west, south, 
east, north-west, north-east, south-west and south-east)

The first version of the `run_simulation` function was done with a `for-loop` that iterated over each generation, 
first cleared the console, then called the `update_world` function to update the world and store the next generation
population states. Lastly the program was delayed by 0.2 milliseconds so that the user actually had time to see the 
different generation ticks.

Then the `update_world` function was implemented. An empty dictionary for the next generation was made.
A `for-loop` then iterated over the coordinates and cells in the input current generation dictionary. A new cell 
dictionary was also made within the `for-loop` for the next generation. Since the rim-cells and ordinary cells 
have different attributes the rim-cells were taken out with an `if-statement`, then printed out with calling the 
`progress` and `get_print_value` functions from the code base with the rim-cell stat as input. 
A newline was also printed after every last rim-cell of each row, using another `if-statement`, so that the
world would not be printed out in a single line. A `continue` was also put in to continue to the next cell. 
To print out the rest of the cells, the `progress` and `get_print_value` functions from the code base was called 
with the cell state as input. The cell states for the next generation was then determined according to the 
rules of transitioning stated in the project guidance, using an `if-statement` and calling the 
`count_alive_neighbours` function. Implementations for grade A was also later done here. New states and neighbours 
was mapped with the coordinates in the next generation dictionary.

In order to complete the `count_alive_neighbours` function, a counter for living neighbours was implemented, then 
with a `for-loop` that looped over each neighbour, the counter was incremented by one for each alive neighbour.

The recursive function of `run_simulation` was then implemented for grade D. This was done by removing the iterative
`for loop` and by adding a line where the function called itself for the next generation.
See the discussion part why this was first implemented even though it was later removed for the grade B requirements.

Then the `load_seed_from_file` function for grade C was completed. The file name needed to be formatted so that the
user could omit the file ending ".json" if wanted. This was done with a simple `if-statement` that controlled
if the user input file name had the proper suffix and otherwise added it. Then a file path was created and with a 
context manager the file could be opened. The data from the JSON files then needed to be formatted in order to comply 
with the code. The world size was formatted to a tuple with the `tuple()` function. A new population dictionary was 
created, cell coordinates were formatted to tuples using `literal_eval` from the ast module, the list of neighbours
were formatted to a list of tuples with the `tuple()` function in a small `for-loop`.

For the grade B requirements, the functions `create_logger` and `simulation_decorator` were completed. 
The `run_simulation` function was yet again changed and decorated to the definition stated in the project guidance.
The `create_logger` function required a logger to be set up at info level. A file path was created to make sure the 
log file was saved in the "Resources" folder according to the project's requirements. A file handler with logging
level info was added to the logger, the mode for how the file should be opened was set to "write mode". In the 
`simulation_decorator` function the logger was created with `create_logger()`, then a new wrapper function named 
`wrapper_function` was created. This function got the inputs of generation, population and world size, just like
the `run_simulation` function. With a `for-loop` that ran over each generation the console was cleared, 
logging information was calculated by counting the entire population and implementing counters for each cell state.
The log output was then formatted with an `f-string`. Then the decorated function was called to store the updated
cell states. Then like in the base implementation the program was delayed by 0.2 milliseconds so that the user 
actually had time to see the different generation ticks.

For the grade A implementation of aging of cells, several functions needed to be adjusted. In `load_seed_from_file` 
and `populate_world` the age key and value of zero was to be added to each cell dictionary. With the added cell 
states of Elders and Prime Elders the `update_world` function now had to include these states when determining the 
age and cell state of the next generation. This was done by updating the `if-statement` to include these states. 
In `count_alive_neighbours` instead of counting only alive neighbours (thus technically not including elders and
prime elders) the function was changed to count all not dead neighbours. The logging information in the
`simulation_decorator` function was also changed to include the new cell states. Like with counting alive neighbours,
since both elders and prime elders are alive, the alive counter was changed to count all not dead cells.


## Discussion

Beginning with the base implementations, the `calc_neighbour_positions`, `run_simulation` and `count_alive_neighbours`
functions were fairly straight forward and easily implemented. Since the program required all base functions to work in
its full extent, not getting an output during development made troubleshooting harder. I depended heavily on PyCharm's 
debugger to help seek out problems within the code.

During the implementation of the `parse_world_size_arg` function a small problem emerged. A ValueError message was 
printed out instead of an AssertionError message because the `.split()` function gave back an empty string if the user
input was "40x". The problem was solved by having the `assertion` sort out empty strings and raise an AssertionError.

The `populate_world` function was a bit trickier to get right. In order to make the output pattern conform with the
provided seed patterns in the code base the axes of (x, y) was flipped to (y, x), again the debugger was a great tool
to see each cell's state, neighbours and how it was printed out. Having a dictionary within a dictionary also took
a while to get my head around.

The `update_world` function was also one of the more challenging functions to implement. I struggled to get the 
line breaks correct since the (y, x) axes were flipped, but managed to get it correct in the end. Getting the 
`if-statement` for determining the state of the next generation was also a challenge. I realized I had too many alive 
cells in the coming generations, since I had accidentally made dead cells with only two alive neighbours live in the 
next generation, this was easily fixed with putting in an `or`.

I decided to do the grade D implementation of making the `run_simulation` a recursive function, even though I knew 
I would later remove it since I strived for a higher grade. This was mostly because I wanted some
more practice on recursive functions, and I knew that I had the extra time. Writing the function was easy, or so I 
thought, my recursive function worked with the tiny problem of that I had created an infinite loop. Even if I put in 
a range, the function would not stop at generation 0. I put in an `if-statement` trying to stop the function at 
generation 0, but I did not know how to stop it and what to return. It took me a while to figure out that it is 
possible to just return (void) and thereby stopping the infinite loop. However, this function was then remade again 
for the grade B implementations.

The challenge with the grade C implementation of the `load_seed_from_file` function was to convert the JSON files and 
thus getting the population dictionary in the correct format. Once again the debugger was of great help to spot out the 
differences. `literal_eval` from the ast module was new to me, but was very handy for converting the coordinates to 
the proper format of tuples.

The grade B implementations was what I found particularly difficult with this project, especially the 
`simulation_decorator` function. Grasping the concept of decorators, the flow of executions, how they work, 
wrappers and how to call what when is challenging even though we worked with decorators during laboration 3. 
Doing the `create_logger` and formatting the logger output was more straight forward and reminded a lot of laboration 3.

The grade A requirements were easier than I expected, and I actually found the functions for grade E and B being 
harder to complete. I suppose that I expected something nearly undoable. I strayed a bit from the note in the project
guidance where it was stated that the age attribute for JSON files was most appropriate to implement during world 
update. Instead, I implemented the age attribute in the `load_seed_from_file` function. For me, it made more 
sense to have it here where the initial population was created. Having completed all the functions I went back over
the entire code again to see if I could do any improvements. I realised that I could shorten a few `if-statements` in 
the `simulation_decorator`, `update_world` and `count_alive_neighbours` functions. They had become quite long to 
include the new cell states of elders and prime elders that also represented aliveness. So instead of setting 
`if-statements` for each cell state, I could set the requirement as not state dead, which shortened the code 
significantly and thus improving readability.


!!!!!!! 
going through the code again, I noticed I was prematurely ageing my newborn cells.
hittade att jag ageade mina celler för fort, newborns måste börja på 0.
skriv hur jag tänker med age, elders prime-elders...

This course has taught me basically everything I have demonstrated with this project, since I knew pretty much nothing
coming in to this course. The learning modules prepared me very well for this project. Being so new to programming, 
I sometimes find it hard to think outside the box, knowing how to improve my code in any way that is not stated in 
the project or laboratory guidance. There are probably ways of further improving the code but considering my 
capabilities I am quite pleased with it. By completing this project and doing all implementations up to grade A, 
I have demonstrated that I can utilize what the learning objectives of this course has taught me, and thereby the 
purpose has been fulfilled. 

