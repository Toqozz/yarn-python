#!/usr/bin/env python3

from time import sleep #Import the sleep function, which allows us to delay prints to stdout.
import argparse #For parsing arguments easily.
import sys #For reading stdin and also using sys.exit to break the program.


def scroll(beginning, str, characters):
    # Definitions
    str2 = ''                    # An additional string to work with [str]
    final = ''                   # A final string to keep track of the characters that are being printed.
    t = True                     # Boolean using in check for starting character.
    array = []                   # List to hold all the strings.

    # We add spaces to the front of the string to make it 'scroll' in from the right.
    # '-' is used in the comment examples so that it is more readable.
    for i in range(0, characters-1):
        str2 = str2 + ' '

    # Create the string '--------hello--------'
    str = str2 + str
    str = str + str2

    for i in range(0, len(str)):
        # This if statement could probably be removed, but it is not doing any harm really being there.
        if str[i] == ' ' and t == True: pass
        else:
            array.append(beginning + final + str[i] + '\n')
            t = False

        # Add the new character to the string.
        final = final + str[i]

        # If the length of final is equal to the maximum number of characters, cut off the first character
        if len(final) > characters-1:
            final = final[1:]

    #if blank == True:
        #for n in range(0, len(array)):
            #array[n] = array[n].replace('-', ' ')

    return array

if __name__ == '__main__':
    array = scroll('summary', 'body text is here', 20)
    for any in array:
        print(any)
