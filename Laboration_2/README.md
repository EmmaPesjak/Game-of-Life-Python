# Laboration 2
Emma Pesjak 2021-09-20
## Environment & Tools
The laboration was performed on a Windows 10 PC with PyCharm 2021.2.1, Python 3.9.7 and Git version 2.33.0.windows.2. 
The sources of information used for this laboration has been course literature
(chapter 2 in Pro Git, second edition and chapter 4-9 in Python Basics, fourth edition), 
[this](https://www.youtube.com/watch?v=W8KRzm-HUcc) video by Corey Schafer and a webpage on ASCII-conversion from
[Stackoverflow](https://stackoverflow.com/questions/227459/how-to-get-the-ascii-value-of-a-character) 
accessed 2021-09-19.

## Purpose
The purpose of laboration 2 was to get an understanding of using and combining strings, loops and different 
functions and to work with user input and validation. 

## Procedures
In `def authenticate_user`, to be able to use the user input in credentials, credentials was split with `.split` 
into given name, surname and password and saved into `user_tmp` and `pass_tmp`.

The function `def format_username` was then completed to format the username so that the given name and surname
started with capital letters, the rest of the letters were lowercase and the names were combined with an underscore and 
then stored in a return value. 
This was done with `.upper` and `.lower` for said indexes. For example, if the user input was cHevY chase, 
the username would be formatted to Chevy_Chase. The `def format_username` was solved differently at first
(quite similar but with an f-string), then checking back in the laboratory guidance there was the `.join` tip, 
so it was changed. 

Then the `def decrypt_password` function was completed using `enumerate` in a for loop with if/else statements to decrypt
the password. Characters at even index positions (determined with a modulus % 2 == 0) were rotated 7, odd 9 according 
to ASCII using `chr` and `ord`. Vowels were preceded and succeeded by 0 in a string. The completed loop was put together 
into the return value "decrypted".

Having both the formatted username and decrypted password, an if-statement was written into the `def authenticate_user`
to check if the username existed in the dictionary and then to see if the key output (the value) was the same as the 
decrypted password.

## Discussion
The laboration was very challenging but fun to do, I really enjoyed the detail and background of the laboratory 
guidance. It also said enough and gave enough tips without being overly obvious on how to solve the problems.

At first, I was a bit overwhelmed by this laboration. I did not know where to start and found the def authenticate_user
part the hardest, even though the code is quite short. I immediately understood that I had to split the credentials, 
but the rest was harder, both trying to figure out the functions worked and how to combine them, knowing what to call 
and what to return. I did a lot of trial and error. The learning modules definitely prepared me for this laboration,
but it was a lot to read and to understand, not all of it "stuck", and I had to go back and read during the laboration.
I do not have any previous experience with programming, so there is a lot of new terms and ways to think. I also 
lack enough experience to see if my code is easily comprehensible. Overall, I think (and hope) that I did a pretty 
good job with the code, it works and the purpose has been fulfilled. The part I am the least content with is 
the `def format_username`. The code is a bit dense, hard to read and looks confusing at first glance, but it does 
the job I suppose. 




