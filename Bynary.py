import curses
import sys
import os

def run_binary_program(bitstream, output_window):
    registers = [0] * 16
    memory = [0] * 256  # 256 bytes of memory
    program_counter = 0
    instructions = [bitstream[i:i+8] for i in range(0, len(bitstream), 8)]

    while program_counter < len(instructions):
        instruction = instructions[program_counter]
        program_counter += 1

        operation = instruction[:4]
        register_index = int(instruction[4:], 2)

        if operation == "0000":  # NOOP - do nothing
            continue

        elif operation == "0001":  # LOAD - load value into register
            value = int(instructions[program_counter], 2)
            program_counter += 1
            registers[register_index] = value

        elif operation == "0010":  # ADD - add 1 to register
            registers[register_index] += 1

        elif operation == "0011":  # SUB - subtract 1 from register
            registers[register_index] -= 1

        elif operation == "0100":  # PRINT - print number
            output_window.addstr(str(registers[register_index]) + "\n")

        elif operation == "0101":  # COPY - copy reg to reg (next byte: source reg in bits 0-3, dest in 4-7)
            next_byte = int(instructions[program_counter], 2)
            program_counter += 1
            source_reg = (next_byte >> 4) & 0x0F
            dest_reg = next_byte & 0x0F
            registers[dest_reg] = registers[source_reg]

        elif operation == "0110":  # JNZ - jump if register not zero
            jump_address = int(instructions[program_counter], 2)
            program_counter += 1
            if registers[register_index] != 0:
                program_counter = jump_address

        elif operation == "0111":  # JMP - jump always
            jump_address = int(instructions[program_counter], 2)
            program_counter += 1
            program_counter = jump_address

        elif operation == "1001":  # PRINTC - print character
            output_window.addstr(chr(registers[register_index]))

        elif operation == "1010":  # INPUT - get character from user and store ASCII value
            curses.echo()
            output_window.addstr("Input: ")
            output_window.refresh()
            char = output_window.getch()
            curses.noecho()
            registers[register_index] = char if char != -1 else 0

        elif operation == "1011":  # ADDR - add two registers (next byte: src1 in bits 0-3, src2 in 4-7, result in current reg)
            next_byte = int(instructions[program_counter], 2)
            program_counter += 1
            src1 = (next_byte >> 4) & 0x0F
            src2 = next_byte & 0x0F
            registers[register_index] = registers[src1] + registers[src2]

        elif operation == "1100":  # SUBR - subtract registers (reg = src1 - src2)
            next_byte = int(instructions[program_counter], 2)
            program_counter += 1
            src1 = (next_byte >> 4) & 0x0F
            src2 = next_byte & 0x0F
            registers[register_index] = registers[src1] - registers[src2]

        elif operation == "1101":  # MULR - multiply registers
            next_byte = int(instructions[program_counter], 2)
            program_counter += 1
            src1 = (next_byte >> 4) & 0x0F
            src2 = next_byte & 0x0F
            registers[register_index] = registers[src1] * registers[src2]

        elif operation == "1110":  # DIVR - divide registers (integer division)
            next_byte = int(instructions[program_counter], 2)
            program_counter += 1
            src1 = (next_byte >> 4) & 0x0F
            src2 = next_byte & 0x0F
            if registers[src2] != 0:
                registers[register_index] = registers[src1] // registers[src2]
            else:
                output_window.addstr("ERROR: Division by zero\n")

        elif operation == "1111":  # Extended operations (next byte determines operation)
            ext_op = int(instructions[program_counter], 2)
            program_counter += 1
            
            if ext_op == 0:  # MOD - modulo (next byte: src1, src2)
                next_byte = int(instructions[program_counter], 2)
                program_counter += 1
                src1 = (next_byte >> 4) & 0x0F
                src2 = next_byte & 0x0F
                if registers[src2] != 0:
                    registers[register_index] = registers[src1] % registers[src2]
                    
            elif ext_op == 1:  # CMP - compare and set flag (sets reg to 1 if src1 < src2, 0 if equal, -1 if >)
                next_byte = int(instructions[program_counter], 2)
                program_counter += 1
                src1 = (next_byte >> 4) & 0x0F
                src2 = next_byte & 0x0F
                if registers[src1] < registers[src2]:
                    registers[register_index] = 1
                elif registers[src1] == registers[src2]:
                    registers[register_index] = 0
                else:
                    registers[register_index] = 255  # -1 in unsigned
                    
            elif ext_op == 2:  # STORE - store register to memory
                addr = int(instructions[program_counter], 2)
                program_counter += 1
                memory[addr] = registers[register_index]
                
            elif ext_op == 3:  # LOAD_MEM - load from memory to register
                addr = int(instructions[program_counter], 2)
                program_counter += 1
                registers[register_index] = memory[addr]
                
            elif ext_op == 4:  # JZ - jump if zero
                jump_address = int(instructions[program_counter], 2)
                program_counter += 1
                if registers[register_index] == 0:
                    program_counter = jump_address
                    
            elif ext_op == 5:  # JLT - jump if less than (reg < 128, treating as signed)
                jump_address = int(instructions[program_counter], 2)
                program_counter += 1
                if registers[register_index] > 127:  # negative in signed 8-bit
                    program_counter = jump_address
                    
            elif ext_op == 6:  # AND - bitwise AND
                next_byte = int(instructions[program_counter], 2)
                program_counter += 1
                src1 = (next_byte >> 4) & 0x0F
                src2 = next_byte & 0x0F
                registers[register_index] = registers[src1] & registers[src2]
                
            elif ext_op == 7:  # OR - bitwise OR
                next_byte = int(instructions[program_counter], 2)
                program_counter += 1
                src1 = (next_byte >> 4) & 0x0F
                src2 = next_byte & 0x0F
                registers[register_index] = registers[src1] | registers[src2]
                
            elif ext_op == 8:  # XOR - bitwise XOR
                next_byte = int(instructions[program_counter], 2)
                program_counter += 1
                src1 = (next_byte >> 4) & 0x0F
                src2 = next_byte & 0x0F
                registers[register_index] = registers[src1] ^ registers[src2]
                
            elif ext_op == 9:  # SHL - shift left
                registers[register_index] = (registers[register_index] << 1) & 0xFF
                
            elif ext_op == 10:  # SHR - shift right
                registers[register_index] = registers[register_index] >> 1
                
            elif ext_op == 11:  # PRINTN - print number without newline
                output_window.addstr(str(registers[register_index]))
                
            elif ext_op == 12:  # INPUTN - input a number
                curses.echo()
                output_window.addstr("Enter number: ")
                output_window.refresh()
                num_str = output_window.getstr(10, 10, 10).decode()
                curses.noecho()
                try:
                    registers[register_index] = int(num_str) & 0xFF
                except:
                    registers[register_index] = 0

        elif operation == "1000":  # END - stop program
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
