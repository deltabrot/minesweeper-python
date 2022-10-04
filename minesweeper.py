import os
from enum import Enum
from random import randint

ERROR_INVALID_INPUT = "Invalid input. Please enter a valid location."

class CellState(Enum):
    NOT_TOUCHED = "not_touched"
    TOUCHED = "touched"
    MINE = "mine"
    EXPLODED = "exploded"

def get_unique_random_location(mine_locations, width, height):
    random_location = None
    is_unique = False
    while not is_unique:
        random_location = [randint(0, width - 1), randint(0, height - 1)]
        if random_location not in mine_locations:
            is_unique = True

    return random_location

def generate_mines(mines, width, height):
    mine_locations = []

    for i in range(mines):
        random_location = get_unique_random_location(mine_locations, width, height)
        mine_locations.append(random_location)

    return mine_locations


def generate_game_state(width, height, mine_locations):
    game_state = []

    for y in range(height):
        row_state = []
        for x in range(width):
            if [x, y] in mine_locations:
                row_state.append(CellState.MINE)
            else:
                row_state.append(CellState.NOT_TOUCHED)
        game_state.append(row_state)

    return game_state

def print_graphic_row(width, start, middle, connector, end):
    print("    %s" % start, end="")
    for x in range(width):
        print(middle * 4, end="")
        if x < width - 1:
            print(connector, end="")
        else:
            print(end, end="")
    print()

def print_game(game_state, column_characters, row_characters):
    width = len(game_state[0])
    height = len(game_state)

    print("      ", end="")
    for i in range(width):
        print(column_characters[i], end="    ")

    print_graphic_row(width, "┌", "─", "┬", "┐")
    print()
    for y in range(height):
        if len(row_characters[y]) == 1:
            print("  %s " % row_characters[y], end="")
        else:
            print(" %s " % row_characters[y], end="")
        for x in range(width):
            match game_state[y][x]:
                case CellState.NOT_TOUCHED:
                    print("│ ░░ ", end="")
                case CellState.TOUCHED:
                    print("│    ", end="")
                case CellState.MINE:
                    print("│ ░░ ", end="")
                case CellState.EXPLODED:
                    print("│ ██ ", end="")
                case _:
                    if len(str(game_state[y][x])) == 1:
                        print("│ %d  " % game_state[y][x], end="")
                    else:
                        print("│ %d " % game_state[y][x], end="")
            if x == width - 1:
                print("│", end="")

        print()
        if y < height - 1:
            print_graphic_row(width, "├", "─", "┼", "┤")
        else:
            print_graphic_row(width, "└", "─", "┴", "┘")
    print()

def get_user_input(row_characters, column_characters):
    is_valid = False

    while not is_valid:
        user_input = input("Enter a location: ")
        if len(user_input) != 2:
            print(ERROR_INVALID_INPUT)
            continue

        user_input = user_input.upper()
        if user_input[0] not in column_characters:
            print(ERROR_INVALID_INPUT)
            continue

        if user_input[1] not in row_characters:
            print(ERROR_INVALID_INPUT)
            continue
        is_valid = True

    return [
        column_characters.index(user_input[0]),
        row_characters.index(user_input[1]),
    ]

def how_many_mines_adjacent(game_state, location):
    x, y = location
    surrounding_cells = [
        [x - 1, y - 1],
        [x, y - 1],
        [x + 1, y - 1],
        [x - 1, y],
        [x + 1, y],
        [x - 1, y + 1],
        [x, y + 1],
        [x + 1, y + 1],
    ]

    mines = 0
    for cell in surrounding_cells:
        if cell[0] < 0 or cell[0] >= len(game_state[0]):
            continue
        if cell[1] < 0 or cell[1] >= len(game_state):
            continue
        if game_state[cell[1]][cell[0]] == CellState.MINE:
            mines += 1

    return mines

def check_cell(game_state, mine_locations, cell):
    if cell[0] < 0 or cell[0] >= len(game_state[0]):
        return
    if cell[1] < 0 or cell[1] >= len(game_state):
        return
    if game_state[cell[1]][cell[0]] == CellState.NOT_TOUCHED:
        adjacent_mines = how_many_mines_adjacent(game_state, cell)
        if adjacent_mines == 0:
            game_state[cell[1]][cell[0]] = CellState.TOUCHED
            check_surrounding_cells(game_state, mine_locations, cell)
        else:
            game_state[cell[1]][cell[0]] = adjacent_mines
            return adjacent_mines
    return 0

def check_surrounding_cells(game_state, mine_locations, location):
    x, y = location
    surrounding_cells = [
        [x - 1, y - 1],
        [x, y - 1],
        [x + 1, y - 1],
        [x - 1, y],
        [x + 1, y],
        [x - 1, y + 1],
        [x, y + 1],
        [x + 1, y + 1],
    ]

    for cell in surrounding_cells:
        check_cell(game_state, mine_locations, cell)

    return None

def update_cell(game_state, mine_locations, location):
    x, y = location

    if [x, y] in mine_locations:
        for mine_location in mine_locations:
            game_state[mine_location[1]][mine_location[0]] = CellState.EXPLODED
        return True

    
    adjacent_mines = check_cell(game_state, mine_locations, location)
    if adjacent_mines == 0:
        check_surrounding_cells(game_state, mine_locations, location)
    return False

def check_for_win(game_state, mine_locations):
    for y in range(len(game_state)):
        for x in range(len(game_state[0])):
            if game_state[y][x] == CellState.NOT_TOUCHED:
                return False
    return True

def main():
    width = 15
    height = 10
    mines = 15

    if width > 26:
        width = 26

    if height > 26:
        height = 26

    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    column_characters = []
    for i in range(width):
        column_characters.append(characters[i])

    row_characters = []
    for i in range(width):
        row_characters.append(characters[i])

    mine_locations = generate_mines(mines, width, height)
    game_state = generate_game_state(width, height, mine_locations)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_game(game_state, column_characters, row_characters)
        location = get_user_input(row_characters, column_characters)
        is_game_over = update_cell(game_state, mine_locations, location)
        if check_for_win(game_state, mine_locations):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_game(game_state, column_characters, row_characters)
            print("You win!")
            break
        if is_game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_game(game_state, column_characters, row_characters)
            print("Game over!")
            break

if __name__ == "__main__":
    main()

