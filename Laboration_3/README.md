# Laboration 3
Emma Pesjak 2021-10-01
## Environment & Tools
The laboration was performed on a Windows 10 PC with PyCharm 2021.2.1, Python 3.9.7 and Git version 2.33.0.windows.2. 
The sources of information used for this laboration has been course literature
(chapters 4-9, 12 in Python Basics, fourth edition), course material from modules 1-6,
and a webpage on string formatting from [Stackabuse](https://stackabuse.com/formatting-strings-with-python/) 
accessed 2021-09-30.

## Purpose
The purpose of laboration 3 was to get an understanding of file handling, loggers, decorators, different types of
functions; iterative and recursive, and to see how to set up a well-structured program. 

## Procedures

The `def fibonacci_memory` was first completed by creating a dictionary to store the sequence number and calculated 
values. Then with an if-statement in the inner function `fib` the sequence numbers and calculated values from the 
recursive function was stored in the dictionary if not in the dictionary already.

To create the logger in `def create_logger` a json file was imported from the resources' library. The json file 
contained custom logger configuration, for console output at info level, and for file input at debug level.

Then the inner wrapper of the `def measurements_decorator` was completed. This function wrapped every fibonacci 
function. An empty list `values` was created for later input of the calculated fibonacci values. 
A timer to mark the start time was put in and the info level logger that stated that the measurements started.
With a `for` loop that iterated over each fibonacci function in the range of `nth_nmb` to 0, the values were
appended to the `values` list. Every fifth iteration was also logged at debug level in an if-statement and the 
`modulus` function. The logger logged both the sequence number and the fibonacci value into a file named ass_3.log.
After the `for` loop a timer for the end time was put in and the duration was calculated into the variable `duration`.
The inner wrapper returned the durations and fibonacci values in tuples.

The `def print_statistics` function was completed by some string formatting to comply with the laboratory guidance.
The table of duration times for each fibonacci function was made with a `for` loop that iterated over the 
`fib_details` dictionary.

The last part to complete was the `def write_to_file` function. File name and fibonacci values were taken out of 
`fib_details` with a `for` loop for each fibonacci function. A context manager (`while open ... as file:`) was put in 
the loop to create/open a file in write mode. A total of three files were created with this loop, one for each fibonacci 
function, named according to the laboratory guidance. The information that was supposed to be written into the file 
according to the study guidance was sequence number with its corresponding fibonacci value. In order to do this
a list for each parameter was created. the `values` list got its information from `fib_details` and the `seq_nr`
got its information from a `while` loop that appended sequence numbers by counting backwards from the `nth_nmb` to 0.
Sequence number and fibonacci value were then written to file with `.write`, this by zipping them together with `zip()`.

#### Edit modified solution:
The variable "RESOURCES" with a path to the resource folder was not being used throughout the program. This file path 
was added in `def create_logger` and `def write_to_file` in order to conform with the laboratory guidance. 

## Discussion

The code works, the purpose has been fulfilled, and I feel that I have learned a lot during this laboration. 
I also feel more confident while coding, it is easier to know what information I need to complete the 
different functions etc. I did not completely follow the pseudocode in the `write to file` part,
I did a `while` loop instead of a `for` loop. I did not quite get a `for` loop to work and found it easier with a 
`while` loop.

I am aware that I probably write too many, and slightly unnecessary # comments. Some comments I write may be
self-explained in the code. This is simply because I want it to be very clear for myself when I go back to my code, 
since I am not a very experienced coder. I struggled a bit with naming variables in the end of the code, many variables
were similar, and I know that it is important to choose appropriate variable names for the code to be easily read.

As with the previous laborations, everything in this one has been new learning for me. Something that was particularly
difficult was the concept of decorators, to see how it all connects. Also, to really understand how the recursive 
functions works by calling themselves.

As usual the modules prepared me well for this laboration, I really appreciate the different learning techniques
with videos, articles and course literature. There could have been a few more, and a bit more challenging exercises for
these two last modules. Perhaps I missed it in the modules, but I did not quite know how to print the statistics with 
left/right justification, this I found online. While this laboration was much more complicated than lab 2, 
for some reason it did not feel as daunting. The previous lab taught me to see the structured code and start 
implementing bit by bit. Another thing I found challenging was that in order to see if the code worked, I had to 
complete several functions to be able to see my output, this also made troubleshooting a bit harder. 

#### Edit modified solution:

I must have completely missed the "RESOURCES" variable during the first implementation, I think I was very focused
on examples from the course literature and not reading the assignment properly.