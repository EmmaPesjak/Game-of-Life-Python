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
has aimed to teach, for example functions, logging, decorators, json-files, file handling etc.


## Procedures
First, the base implementations for grade E was completed, beginning with the `parse_world_size_arg` function. 
The user input was a string with the format width x height. And the function needed to convert this into integers in 
a tuple. By splitting the string input at the "x" with the `.split()` function into a width_height variable, 
values for width and height could be extracted. But first in a `try` block, with an `assert-statement` 
the user input was validated with the help of the `len()` function to see that the user had not written too few 
or too many values, it had to be for example 80x40. Width and height were extracted from the width_height 
variable and converted to integers with the `int()` function. With an `if-statement` a ValueError would be raised 
if either height or width were below one. With an `except`, if the user input was for any reason incorrect the program 
would write an assert message or an error message in the console and use the default value of 80x40.


`populate_world`



def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    population = {}

    pattern = cb.get_pattern(_seed_pattern, _world_size)
    width_coords = range(_world_size[0])
    height_coords = range(_world_size[1])
    coordinates = itertools.product(height_coords, width_coords)

    # Axes are flipped (y, x) to conform with provided seed patterns in code base.
    for y, x in coordinates:
        cell = {}
        # Declare rim cells.
        if x == 0 or y == 0 or x == (_world_size[0] - 1) or y == (_world_size[1] - 1):
            population[(y, x)] = None       # Store in population dictionary.
            continue
        # In case of seed pattern, set cell state to live or dead according to
        # coordinates in code base.
        if pattern is not None:
            if (y, x) in pattern:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD
        # Randomize cell state if no pattern is to be used.
        else:
            random_cell = random.randint(0, 20)
            if random_cell > 16:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD

        # Map cell state, neighbours and age to cell dictionary, then map coordinates
        # and cell dictionary to population dictionary.
        cell["state"] = state
        cell["neighbours"] = calc_neighbour_positions((y, x))
        cell["age"] = 0
        population[(y, x)] = cell
    return population



The `calc_neighbour_positions` function was then completed simply by getting the coordinates from the 
input "_cell_coord" and putting these into the variables y and x. This might seem backwards but the axes were flipped 
in order to conform with the provided seed patterns in the code base. The function then returned a list of tuples
with the neighbours coordinates calculated by offsetting their positions in all directions (north, west, south, 
east, north-west, north-east, south-west and south-east)

The first version of the `run_simulation` function was done with a `for-loop` that iterated over each generation, 
first cleared the console, then called the `update_world` function to update the world and store the next generation
population states. Lastly the program was delayed by 0.2 milliseconds so that the user actually had time to see the 
different generation ticks.


`update_world`



def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    next_gen = {}
    for coords_, cell in _cur_gen.items():
        new_cell = {}
        # Print rim cell, print new line after every last rim cell of each row,
        # update next generation dictionary.
        if cell is None:
            cb.progress(cb.get_print_value(cb.STATE_RIM))
            if coords_[1] == (_world_size[0] - 1):
                cb.progress("\n")
            next_gen[coords_] = cell
            continue

        # Print cell that is not rim cell.
        cb.progress(cb.get_print_value(cell["state"]))

        # Determine next generation cell state and age, store in new cell dictionary.
        if (cell["state"] != cb.STATE_DEAD and
            count_alive_neighbours(cell["neighbours"], _cur_gen) == 2) \
                or (count_alive_neighbours(cell["neighbours"], _cur_gen) == 3):
            new_cell["age"] = (cell["age"] + 1)
            if new_cell["age"] > 10:
                new_cell["state"] = cb.STATE_PRIME_ELDER
            elif new_cell["age"] > 4:
                new_cell["state"] = cb.STATE_ELDER
            else:
                new_cell["state"] = cb.STATE_ALIVE
        else:
            new_cell["state"] = cb.STATE_DEAD
            new_cell["age"] = 0

        # Store the neighbours for next generation and update next generation dictionary.
        new_cell["neighbours"] = cell["neighbours"]
        next_gen[coords_] = new_cell
    return next_gen



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

parse_world_size_arg
had trouble with wrong error message when empty string from .split
assert was hard to grasp since it is "backwards thinking".

completed the base implementations 
populate_world

calc_neighbour_positions
this was the most straigt forward function, basically nothing hard, just make a list of tuples of neighbours

run_simulation
also pretty straight forward

update_world
None cells easy fix
tricky to get the neighbours count right for next gen

count_alive_neighbours

grade d recursive
did not know you could return (void) this caused a hick-up

grade c load seed from file
pretty straight forward to implement but getting the population dictionary correct was a bit of a challenge.


grade a la till age i jsonfilerna i annan funktion än den som stod skriven i labhandledningen.
tbh grade a was suprisingly easy, was expecting something much more harder. i suppose every one has their own oppinions 
but i found both grade e and grade b implementations harder than grade a. 

`parse_world_size_arg`

`populate_world`

`calc_neighbour_positions`

`run_simulation`

`update_world`

`count_alive_neighbours`
`load_seed_from_file`
`create_logger` and `simulation_decorator`

furthermore...



## Purpose / Syfte
Perspective: What does the assignment aim to accomplish?
Should specify concrete goal(s) which will enable some discussion and analysis.
## Procedures / Genomförande
Perspective: How can the results (solution) be reproduced?
What kind of problems emerged and how were these resolved?
## Discussion / Diskussion
Perspective: Has the purpose been fulfilled? Determine the suitability of the implementation...
should alternative approaches and procedures be considered?
Personal reflections: What did you learn? What did you find to be particularly difficult? Did the
learning module(s) prepare you sufficiently for the challenge? What could be improved in regards to
the assignment? Etc.
