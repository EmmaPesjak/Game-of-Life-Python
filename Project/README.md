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
would write the assert or error message in the console and use the default value of 80x40.

The next step was to complete the `populate_world` function which created the initial population of cells.
An empty population dictionary was created to be later filled in. In case of that the user would use a seed pattern the 
`get_pattern` function from the code base was called and stored in the variable pattern. Width and height coordinates
were extracted from the world size tuple input, and to get every coordinate the `range()` function was used. With
`itertools product()` the coordinates were matched together for each row and column. Then a `for-loop` that iterated 
over the coordinates was done. In order to conform with the provided seed patterns in the code base, the axes of 
the coordinates were flipped to (y, x). Another cell dictionary was created since the population dictionary had
the coordinates as keys and the cell dictionary as values, the cell dictionary contained the cells states and 
neighbours (and later also age for the grade A implementation). The edge of the world, to define the border consisted 
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

Beginning with the base implementations.... `calc_neighbour_positions``run_simulation``count_alive_neighbours` easy, hard part was not getting an output until 
many functions done, i depended heavily on the debugger function in PyCharm to seek out problems with my code

During the implementation of the `parse_world_size_arg` function a small problem emerged. A ValueError message was 
printed out instead of an AssertionError message because the `.split()` function gave back an empty string if the user
input was "40x". The problem was solved by having the assert sort out empty strings and raise an AssertionError.

`populate_world`
flippade axes

`update_world`
None cells easy fix
tricky to get the neighbours count right for next gen

grade d recursive
did not know you could return (void) this caused a hick-up

grade c `load_seed_from_file`
pretty straight forward to implement but getting the population dictionary correct was a bit of a challenge.

grade b`create_logger` and `simulation_decorator`

grade a la till age i jsonfilerna i annan funktion än den som stod skriven i labhandledningen.
tbh grade a was suprisingly easy, was expecting something much more hard. i suppose every one has their own opinions 
but i found both grade e and grade b implementations harder than grade a. 

went back over the entire code to see if i could do any improvements, shortened a bit by writing != dead instead
of alive + elders + primes

i have learned..

being so new to programming, i sometimes find it hard to think outside the box, knowing how to improve my code
out of the boundaries of the project or laboratory guidance.

the learning modules prepared....

furthermore...

By completing this project and doing all implementations up to grade A, I have demonstrated that I can utilize the
learning objectives of this course, and thereby the purpose has been fulfilled. 
