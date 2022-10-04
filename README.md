# minesweeper-python

An example of minesweeper written in (Python)[https://www.python.org/] which can
be played in a terminal

## How to run

To play the game, first clone this repository, open a terminal, and navigate to
the repository location, then run:
```bash
python minesweeper.py
```

## How to play

To make it possible to have a larger grid, you must select the cell you want to
check using two letters of the alphabet. The first letter determines the
horizontal position, the second letter determines the vertical position.

For example, if I wanted to try 5 along, and 3 down, I would type:
```
Enter a location: EC
```

**Note:** The input is case insensitive, so you could also input `ec`.

## Changing the size of the board

There are two variables defined in the `main()` function in `minesweeper.py`,
`width` and `height`. Modifying these will affect the size of the board.

## Additional notes

There is currently no way to place a "flag" in a cell, however you will receive
a win message if you manage to successfully identify all clear cells.
