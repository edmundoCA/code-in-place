RUBIK_COLORS = ("yellow", "white", "orange", "red", "blue", "green")
RUBIK_FACES = ("up", "down", "left", "right", "front", "back")
rubik_cube = {}

def main():
    set_initial_state()
    move_U_prime()
    move_D_prime()
    display_in_console_pretty()
    move_R()
    display_in_console_pretty()

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
        rubik_cube["down"][2-i][2] = rubik_cube["back"][i][0]
        rubik_cube["back"][i][0] = rubik_cube["up"][i][2]
        rubik_cube["up"][i][2] = memory
    for i in range(2):
        memory = rubik_cube["right"][0][i]
        rubik_cube["right"][0][i] = rubik_cube["right"][2-i][0]
        rubik_cube["right"][2-i][0] = rubik_cube["right"][2][2-i]
        rubik_cube["right"][2][2-i] = rubik_cube["right"][i][2]
        rubik_cube["right"][i][2] = memory

def move_L():
    for i in range(3):
        memory = rubik_cube["front"][i][0]
        rubik_cube["front"][i][0] = rubik_cube["up"][i][0]
        rubik_cube["up"][i][0] = rubik_cube["back"][i][0]
        rubik_cube["back"][i][0] = rubik_cube["down"][i][0]
        rubik_cube["down"][i][0] = memory

def move_U():
    for i in range(3):
        memory = rubik_cube["front"][0][i]
        rubik_cube["front"][0][i] = rubik_cube["right"][0][i]
        rubik_cube["right"][0][i] = rubik_cube["back"][0][i]
        rubik_cube["back"][0][i] = rubik_cube["left"][0][i]
        rubik_cube["left"][0][i] = memory

def move_D():
    for i in range(3):
        memory = rubik_cube["front"][2][i]
        rubik_cube["front"][2][i] = rubik_cube["left"][2][i]
        rubik_cube["left"][2][i] = rubik_cube["back"][2][i]
        rubik_cube["back"][2][i] = rubik_cube["right"][2][i]
        rubik_cube["right"][2][i] = memory

def move_F():
    for i in range(3):
        memory = rubik_cube["up"][2][i]
        rubik_cube["up"][2][i] = rubik_cube["left"][-i][2]
        rubik_cube["left"][-i][2] = rubik_cube["down"][0][-i]
        rubik_cube["down"][0][-i] = rubik_cube["right"][i][0]
        rubik_cube["right"][i][0] = memory

def move_B():
    for i in range(3):
        memory = rubik_cube["up"][0][-i]
        rubik_cube["up"][0][-i] = rubik_cube["right"][-i][2]
        rubik_cube["right"][-i][2] = rubik_cube["down"][2][i]
        rubik_cube["down"][2][i] = rubik_cube["left"][i][0]
        rubik_cube["left"][i][0] = memory

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