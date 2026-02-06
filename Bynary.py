import curses
import sys
import os

def run_binary_program(bitstream, output_window):
    registers = [0] * 16
    program_counter = 0
    instructions = [bitstream[i:i+8] for i in range(0, len(bitstream), 8)]

    while program_counter < len(instructions):
        instruction = instructions[program_counter]
        program_counter += 1

        operation = instruction[:4]
        register_index = int(instruction[4:], 2)

        if operation == "0000":  # No operation
            continue

        elif operation == "0001":  # Load value into register
            value = int(instructions[program_counter], 2)
            program_counter += 1
            registers[register_index] = value

        elif operation == "0010":  # Add 1 to register
            registers[register_index] += 1

        elif operation == "0011":  # Subtract 1 from register
            registers[register_index] -= 1

        elif operation == "0100":  # Print register as number
            output_window.addstr(str(registers[register_index]) + "\n")

        elif operation == "1001":  # Print register as character
            output_window.addstr(chr(registers[register_index]))

        elif operation == "1000":  # End program
            break

        else:
            output_window.addstr("Invalid instruction\n")
            break

def binary_editor(main_screen, filename=None):
    curses.curs_set(1)
    main_screen.clear()

    text_lines = [""]
    current_filename = filename

    if filename and os.path.exists(filename):
        with open(filename, "r") as file:
            text_lines = file.read().splitlines()
            if not text_lines:
                text_lines = [""]

    cursor_row, cursor_column = 0, 0

    while True:
        main_screen.clear()
        screen_height, screen_width = main_screen.getmaxyx()

        for line_number, line_content in enumerate(text_lines):
            if line_number < screen_height - 2:
                main_screen.addstr(line_number, 0, f"{line_number+1:03} {line_content}")

        name_display = current_filename if current_filename else "Untitled"
        status_line = f"{name_display} | Ctrl+S Save | Ctrl+A Save As | Ctrl+R Run | Ctrl+Q Quit"
        main_screen.addstr(screen_height - 1, 0, status_line[:screen_width - 1])

        main_screen.move(cursor_row, cursor_column + 4)
        main_screen.refresh()

        key_pressed = main_screen.getch()

        if key_pressed == 17:  # Ctrl+Q to quit
            break

        elif key_pressed == 19:  # Ctrl+S to save
            if not current_filename:
                main_screen.addstr(screen_height - 2, 0, "No filename. Use Ctrl+A to Save As.")
            else:
                with open(current_filename, "w") as file:
                    file.write("\n".join(text_lines))

        elif key_pressed == 1:  # Ctrl+A for save as
            curses.echo()
            main_screen.addstr(screen_height - 2, 0, "Save as: ")
            main_screen.clrtoeol()
            new_filename = main_screen.getstr(screen_height - 2, 9, 60).decode()
            curses.noecho()
            if new_filename:
                current_filename = new_filename
                with open(current_filename, "w") as file:
                    file.write("\n".join(text_lines))

        elif key_pressed == 18:  # Ctrl+R to run
            output_screen = curses.newwin(screen_height, screen_width, 0, 0)
            output_screen.clear()
            all_bits = "".join(char for char in "".join(text_lines) if char in "01")

            if len(all_bits) % 8 != 0:
                output_screen.addstr("ERROR: bit length not multiple of 8\n")
            else:
                run_binary_program(all_bits, output_screen)

            output_screen.addstr("\n\nPress any key to return...")
            output_screen.refresh()
            output_screen.getch()

        elif key_pressed == 10:  # Enter key
            text_lines.insert(cursor_row + 1, "")
            cursor_row += 1
            cursor_column = 0

        elif key_pressed in (8, 127):  # Backspace
            if cursor_column > 0:
                current_line = text_lines[cursor_row]
                text_lines[cursor_row] = current_line[:cursor_column-1] + current_line[cursor_column:]
                cursor_column -= 1
            elif cursor_row > 0:
                cursor_column = len(text_lines[cursor_row - 1])
                text_lines[cursor_row - 1] += text_lines[cursor_row]
                text_lines.pop(cursor_row)
                cursor_row -= 1

        elif key_pressed == curses.KEY_UP and cursor_row > 0:
            cursor_row -= 1
            cursor_column = min(cursor_column, len(text_lines[cursor_row]))

        elif key_pressed == curses.KEY_DOWN and cursor_row < len(text_lines) - 1:
            cursor_row += 1
            cursor_column = min(cursor_column, len(text_lines[cursor_row]))

        elif key_pressed == curses.KEY_LEFT and cursor_column > 0:
            cursor_column -= 1

        elif key_pressed == curses.KEY_RIGHT and cursor_column < len(text_lines[cursor_row]):
            cursor_column += 1

        elif key_pressed in (ord("0"), ord("1")):
            current_line = text_lines[cursor_row]
            text_lines[cursor_row] = current_line[:cursor_column] + chr(key_pressed) + current_line[cursor_column:]
            cursor_column += 1

def main_program(stdscr):
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    binary_editor(stdscr, filename)

curses.wrapper(main_program)
