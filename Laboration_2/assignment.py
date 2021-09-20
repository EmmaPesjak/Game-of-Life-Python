#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 2
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - authenticate_user(..)
 - format_username(..)
 - decrypt_password(..)
"""

import argparse
import sys

__version__ = '1.0'
__desc__ = "A simple script used to authenticate spies!"


def authenticate_user(credentials: str) -> bool:
    """Procedure for validating user credentials"""
    agents = {  # Expected credentials. MAY NOT BE MODIFIED!!
        'Chevy_Chase': 'i0J0u0j0u0J0Zys0r0{',   # cipher: bAnanASplit
        'Dan_Aykroyd': 'i0N00h00^0{b',          # cipher: bEaUtY
        'John_Belushi': 'j0J0sc0v0w0L0',        # cipher: cAlZonE
    }
    user_tmp = pass_tmp = str()

    ''' PSEUDO CODE
    PARSE string value of 'credentials' into its components: username and password.
    SEND username for FORMATTING by utilizing devoted function. Store return value in 'user_tmp'.
    SEND password for decryption by utilizing devoted function. Store return value in 'pass_tmp'.
    VALIDATE that both values corresponds to expected credentials existing within dictionary.
    RETURN outcome of validation as BOOLEAN VALUE.
    '''
    # Separate username and password from credentials
    credentials_split = credentials.split(" ")
    user_tmp = format_username(credentials_split[0:2])
    pass_tmp = decrypt_password(credentials_split[2])

    # Check in dictionary if credentials are valid.
    if user_tmp in agents:
        return agents[user_tmp] == pass_tmp     # Check if value in dictionary and password are the same.


def format_username(username: list) -> str:
    """Procedure to format user provided username"""

    ''' PSEUDO CODE
    FORMAT first letter of given name to be UPPERCASE.
    FORMAT first letter of surname to be UPPERCASE.
    REPLACE empty space between given name and surname with UNDERSCORE '_'
    RETURN formatted username as string value.
    '''

    # Username is always given name and surname. Since the input is
    # case-insensitive we need to format the username so that given name and
    # surname has capitalized first letters, the rest of the letters are lowercase
    # and the names are combined with an underscore.
    username[0] = username[0][0].upper() + username[0][1:].lower()
    username[1] = username[1][0].upper() + username[1][1:].lower()
    return "_".join(username)

def decrypt_password(password: str) -> str:
    """Procedure used to decrypt user provided password"""
    rot7, rot9 = 7, 9       # Rotation values. MAY NOT BE MODIFIED!!
    vowels = 'AEIOUaeiou'   # MAY NOT BE MODIFIED!!
    decrypted = str()

    ''' PSEUDO CODE
    REPEAT {
        DETERMINE if char IS VOWEL.
        DETERMINE ROTATION KEY to use.
        DETERMINE decryption value
        ADD decrypted value to decrypted string
    }
    RETURN decrypted string value
    '''

    # Decrypt password. Characters at even index positions are rotated 7, odd 9.
    # Vowels are preceded and succeeded by 0.
    for index, char in enumerate(password):
        if index % 2 == 0:                      # Determine if character is at even or odd index position.
            j = chr(ord(char) + rot7)           # Rotate according to ASCII.
        else:
            j = chr(ord(char) + rot9)           # Rotate according to ASCII.
        if char in vowels:                      # Determine if character is a vowel.
            j = str("0" + j + "0")              # Put 0 before and after vowel.
        decrypted = decrypted + j               # Put together all characters into a single password.
    return decrypted

def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT0179G Assignment 2 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('credentials', metavar='credentials', type=str,
                        help="Username and password as string value")

    args = parser.parse_args()

    if not authenticate_user(args.credentials):
        print("Authentication failed. Program exits...")
        sys.exit()

    print("Authentication successful. User may now access the system!")


if __name__ == "__main__":
    main()
