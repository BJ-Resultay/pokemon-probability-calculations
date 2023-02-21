#!/usr/bin/env python3
"""
Class:  CS 460G
Author: BJ Resultay
Date:   6 Feb 2023
File:   dummy_data.py
        create dummy data subfolder and files:
        alphabetical-pokemon.txt
        bot-data.txt
        results.csv
"""
import os
import re
import sys

PARENT_DIR = "../"
MOVES = "moves.txt"
BOT_DATA = "bot-data.txt"
ABC_POKEMON = "alphabetical-pokemon.txt"

class InvalidArgumentError(Exception):
    """Raised when invalid number of arguments are passed"""
    __module__ = Exception.__module__

class InvalidKeywordError(Exception):
    """Raised when invalid keyword is passed"""
    __module__ = Exception.__module__


def main():
    # get keyword
    if len(sys.argv) != 2:
        raise InvalidArgumentError(
            "./dummy_data.py keyword")
    keyword = sys.argv[1]
    
    # clean input
    keyword = keyword.replace(" ", "-")         # replace spaces/underscores with dashes
    keyword = keyword.replace("_", "-")         # used in directory name
    pattern = re.sub(r'[^a-zA-Z]', '', keyword) # remove any nonalphabetical characters
                                                # used in search
    # check pattern is valid
    validatePattern(pattern)

    # create directory
    createDirectory(keyword)

    # populate directory
    DUMMY_DIR = "./" + keyword + "/"
    
    # alphabetical-pokemon
    pokemon = getKeyPokemon(pattern)
    with open(PARENT_DIR + ABC_POKEMON, 'r') as ifile:
        with open(DUMMY_DIR + ABC_POKEMON, 'w') as ofile:
#            ofile.write(createHeader())
            lines = ifile.readlines()
            if "Aerodactyl" not in pokemon:     # control variable
                ofile.write(lines[0])
            for line in lines:
                if line.split()[0] in pokemon:
                    ofile.write(line)
    
    # bot-data
    with open(PARENT_DIR + BOT_DATA, 'r') as ifile:
        with open(DUMMY_DIR + BOT_DATA, 'w') as ofile:
#            ofile.write(createHeader())
            pattern1 = re.compile(r"^Aerodactyl.*(" + "|".join(pokemon) + r")")
            pattern2 = re.compile(r"^(" + "|".join(pokemon) + r").*Aerodactyl") # probably could refactor
            lines = ifile.readlines()
            for i, line in enumerate(lines):
                if pattern1.match(line):
                    ofile.write(line)
                    ofile.write(lines[i+1])     # Possible damage amounts:
                    ofile.write("\n")
                elif pattern2.match(line):
                    ofile.write(line)
                    ofile.write(lines[i+1])     # Possible damage amounts:
                    ofile.write("\n")


def validatePattern(pattern):
    with open(PARENT_DIR + MOVES, 'r') as ifile:
        if pattern == "" or \
            pattern.lower() not in ifile.read().lower():
            raise InvalidKeywordError(
                f"\"{pattern}\" not found")


def createDirectory(keyword):
    mode = 0o755
    path = os.path.join("./", keyword)
#    print(path)
    if not os.path.exists(path):
        os.mkdir(path, mode)


def getKeyPokemon(pattern):
    pokemon = set()
    with open(PARENT_DIR + BOT_DATA, 'r') as ifile:
        lines = ifile.readlines()
        for line in lines:
            if re.search(pattern, line, re.IGNORECASE):
                # pokemon1 keyword vs. pokemon2:
                pokemon.add(line.split()[0])
#    print(len(pokemon))
#    print(pokemon)
    return pokemon


if __name__ == '__main__':
    main()
