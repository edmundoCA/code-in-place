import re
import random

RUBIK_COLORS = ("yellow", "white", "orange", "red", "blue", "green")
RUBIK_FACES = ("up", "down", "left", "right", "front", "back")
MOVES = [
    "R", "R'", "R2", "L", "L'", "L2",
    "U", "U'", "U2", "D", "D'", "D2",
    "F", "F'", "F2", "B", "B'", "B2"
]
FACES_TO_LOOK_UP = ("back", "right", "front", "left")

rubik_cube = {}
daisy = {}
GOD_S_NUMBER = 20

CUBE_IN_A_CUBE_IN_A_CUBE_PATTERN = "U' L' U' F' R2 B' R F U B2 U B' L U' F U R F'"
CUBE_IN_A_CUBE_IN_A_CUBE_INVERSE_PATTERN = "F R' U' F' U L' B U' B2 U' F' R' B R2 F U L U"

def main():
    set_initial_state()
    # SAMPLE_SCRAMBLE = "R2 L U D' L D2 B R U R B' U' F R2 D U B'"
    SAMPLE_SCRAMBLE = "L2 D' U' B' U' R L2 B2 F B D' U' F L2 D B"
    # SAMPLE_SCRAMBLE = "F L2 D B2 R2 L2 F B U2 B' L' F2 L' F"
    # SAMPLE_SCRAMBLE = "D L' B' U' F2 R2 U2 F D2 L' R2 B F2 U"
    play_movements(SAMPLE_SCRAMBLE)
    display_in_console_pretty()
    solve_rubik_s_cube()
    display_in_console_pretty()

def solve_rubik_s_cube():
    solve_layer_one()
    solve_the_middle_layer()
    solve_the_final_layer()

def solve_layer_one():
    create_a_daisy()

def create_a_daisy():
    look_at_the_top_layer()
    print(daisy)
    while are_white_edges_at_the_middle_layer():
        move_petals_from_the_middle_layer()
    print(daisy)

def move_petals_from_the_middle_layer():
    PRIME_MOVES = [move_R_prime, move_F_prime, move_L_prime, move_B_prime]
    MOVES = [move_L, move_B, move_R, move_F]
    for i in range(len(FACES_TO_LOOK_UP)):
        if is_color_tile_at("white", FACES_TO_LOOK_UP[i], 1, 2):
            previous_index = (i - 1) % 4
            previous_face = FACES_TO_LOOK_UP[previous_index]
            count_turns = 0
            while daisy[previous_face] and count_turns < 4:
                turn_daisy()
                count_turns += 1
            MOVES[i]()
            daisy[previous_face] = True
        if is_color_tile_at("white", FACES_TO_LOOK_UP[i], 1, 0):
            next_index = (i + 1) % 4
            next_face = FACES_TO_LOOK_UP[next_index]
            count_turns = 0
            while daisy[next_face] and count_turns < 4:
                turn_daisy()
                count_turns += 1
            PRIME_MOVES[i]()
            daisy[next_face] = True

def turn_daisy():
    petal_in_memory = daisy["front"]
    daisy["front"] = daisy["right"]
    daisy["right"] = daisy["back"]
    daisy["back"] = daisy["left"]
    daisy["left"] = petal_in_memory
    move_U()

def is_color_tile_at_edge(color, front_face, row_front, col_front, side_face, row_side, col_side):
    return (rubik_cube[front_face][row_front][col_front] == color
            or rubik_cube[side_face][row_side][col_side] == color)

def is_color_tile_at(color, front_face, row_front, col_front):
    return rubik_cube[front_face][row_front][col_front] == color

def look_at_the_top_layer():
    daisy["back"] = is_color_tile_at_edge("white", "up", 0, 1, "back", 0, 1) # 12 o'clock
    daisy["right"] = is_color_tile_at_edge("white", "up", 1, 2, "right", 0, 1) # 3 o'clock
    daisy["front"] = is_color_tile_at_edge("white", "up", 2, 1, "front", 0, 1) # 6 o'clock
    daisy["left"] = is_color_tile_at_edge("white", "up", 1, 0, "left", 0, 1) # 9 o'clock

def are_white_edges_at_the_middle_layer():
    return (is_color_tile_at_edge("white", "back", 1, 0, "right", 1, 2)
            or is_color_tile_at_edge("white", "right", 1, 0, "front", 1, 2)
            or is_color_tile_at_edge("white", "front", 1, 0, "left", 1, 2)
            or is_color_tile_at_edge("white", "left", 1, 0, "back", 1, 2))

def solve_the_middle_layer():
    pass

def solve_the_final_layer():
    pass

def get_scrambling_movements():
    INITIAL_DISTANCE = 0
    INITIAL_MOVES = []
    moves = get_scrambling_moves(INITIAL_DISTANCE, INITIAL_MOVES)
    return " ".join(moves)

def get_scrambling_moves(distance, moves):
    if distance >= GOD_S_NUMBER:
        return moves
    move = random.choice(MOVES)
    if distance > 0 and move[0] == moves[len(moves) - 1][0]:
        return get_scrambling_moves(distance, moves)
    if "2" in move:
        distance += 1
    distance += 1
    moves.append(move)
    return get_scrambling_moves(distance, moves)

def parse_moves(movements):
    movements_parsed = movements.replace(" ", "").upper()
    # looks for double movements, e.g. R2
    double_movements_pattern = re.compile(r"(\w)(2)")
    movements_parsed = double_movements_pattern.sub(lambda match: match.group(1) * int(match.group(2)), movements_parsed)
    # looks for single moves, e.g. U or U'
    moves_pattern = re.compile(r"(\w'?)")
    moves = moves_pattern.findall(movements_parsed)
    return moves

def play_movements(movements):
    ALLOWED_MOVES = {
        "R": move_R, "R'": move_R_prime,
        "L": move_L, "L'": move_L_prime,
        "U": move_U, "U'": move_U_prime,
        "D": move_D, "D'": move_D_prime,
        "F": move_F, "F'": move_F_prime,
        "B": move_B, "B'": move_B_prime,
    }
    moves = parse_moves(movements)
    for move in moves:
        ALLOWED_MOVES[move]()

def display_in_console():
    for key in rubik_cube.keys():
        print("_________")
        print(key)
        print("---------")
        for row in rubik_cube[key]:
            print(row)

def move_R():
    for i in range(3):
        memory = rubik_cube["front"][i][2]
        rubik_cube["front"][i][2] = rubik_cube["down"][i][2]
        rubik_cube["down"][i][2] = rubik_cube["back"][2-i][0]
        rubik_cube["back"][2-i][0] = rubik_cube["up"][i][2]
        rubik_cube["up"][i][2] = memory
    rotate_face("right")

def rotate_face(face):
    for i in range(2):
        memory = rubik_cube[face][0][i]
        rubik_cube[face][0][i] = rubik_cube[face][2-i][0]
        rubik_cube[face][2-i][0] = rubik_cube[face][2][2-i]
        rubik_cube[face][2][2-i] = rubik_cube[face][i][2]
        rubik_cube[face][i][2] = memory

def move_L():
    for i in range(3):
        memory = rubik_cube["front"][i][0]
        rubik_cube["front"][i][0] = rubik_cube["up"][i][0]
        rubik_cube["up"][i][0] = rubik_cube["back"][2-i][2]
        rubik_cube["back"][2-i][2] = rubik_cube["down"][i][0]
        rubik_cube["down"][i][0] = memory
    rotate_face("left")

def move_U():
    for i in range(3):
        memory = rubik_cube["front"][0][i]
        rubik_cube["front"][0][i] = rubik_cube["right"][0][i]
        rubik_cube["right"][0][i] = rubik_cube["back"][0][i]
        rubik_cube["back"][0][i] = rubik_cube["left"][0][i]
        rubik_cube["left"][0][i] = memory
    rotate_face("up")

def move_D():
    for i in range(3):
        memory = rubik_cube["front"][2][i]
        rubik_cube["front"][2][i] = rubik_cube["left"][2][i]
        rubik_cube["left"][2][i] = rubik_cube["back"][2][i]
        rubik_cube["back"][2][i] = rubik_cube["right"][2][i]
        rubik_cube["right"][2][i] = memory
    rotate_face("down")

def move_F():
    for i in range(3):
        memory = rubik_cube["up"][2][i]
        rubik_cube["up"][2][i] = rubik_cube["left"][2-i][2]
        rubik_cube["left"][2-i][2] = rubik_cube["down"][0][2-i]
        rubik_cube["down"][0][2-i] = rubik_cube["right"][i][0]
        rubik_cube["right"][i][0] = memory
    rotate_face("front")

def move_B():
    for i in range(3):
        memory = rubik_cube["up"][0][2-i]
        rubik_cube["up"][0][2-i] = rubik_cube["right"][2-i][2]
        rubik_cube["right"][2-i][2] = rubik_cube["down"][2][i]
        rubik_cube["down"][2][i] = rubik_cube["left"][i][0]
        rubik_cube["left"][i][0] = memory
    rotate_face("back")

def move_R_prime():
    for _ in range(3):
        move_R()

def move_L_prime():
    for _ in range(3):
        move_L()

def move_U_prime():
    for _ in range(3):
        move_U()

def move_D_prime():
    for _ in range(3):
        move_D()

def move_F_prime():
    for _ in range(3):
        move_F()

def move_B_prime():
    for _ in range(3):
        move_B()

def display_in_console_pretty():
    face_console_output = " " * 8 + "-" * 9 + "\n"
    face_console_output += generate_face_console_output("up")
    face_console_output += "-" * 33

    for row in range(3):
        row_console_output = "\n"
        for face in ["left", "front", "right", "back"]:
            row_console_output += "| "
            for col in rubik_cube[face][row]:
                row_console_output += col[0] + " "
        row_console_output += "|"
        face_console_output += row_console_output
    print(face_console_output)

    face_console_output = "-" * 33 + "\n"
    face_console_output += generate_face_console_output("down")
    face_console_output += " " * 8 + "-" * 9
    print(face_console_output)

def generate_face_console_output(face):
    face_console_output = ""
    for row in rubik_cube[face]:
        row_console_output = " " * 8 + "| "
        for col in row:
            row_console_output += col[0] + " "
        row_console_output += "|"
        face_console_output += row_console_output + "\n"
    return face_console_output
            
def set_initial_state():
    for face, color in zip(RUBIK_FACES, RUBIK_COLORS):
        rubik_cube[face] = [[color for _ in range (3)] for _ in range (3)]

if __name__ == '__main__':
    main()