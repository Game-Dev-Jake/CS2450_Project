# CS2450_Project

## How to Use
Upon running main.py, UVSim will automatically initialize a CPU, a 100 word memory, and an accumulator. The following option hierarchy will be presented to the user, and will require numbered input to select each option. Each input only requires the first character to contain the proper number option: 

1] Load a file--------------Displays the file loading menu to the user.
    1] Load local file------Scans the UVSim_Files directory and displays the list of found files.
        0-x] Load file------Selects a specific file to load, and attempts to read and push each line into memory.
    2] Exit-----------------Returns to the main menu. 
2] Display values-----------Displays the display menu to the user.
    1] Display Accumulator--Displays the current value loaded into the accumulator.
    2] Display Memory-------Iterates through all 100 memory locations and displays each value to the user.
3] Run Program--------------Begins executing program from memory address 0.
4] Exit---------------------Terminates the program.

## Functions

| Function | Opcode | Description |
|---|---:|---|
| `READ` | `10` | Read a word from the keyboard into a specific memory location. |
| `WRITE` | `11` | Write a word from a specific memory location to screen. |
| `LOAD` | `20` | Load a word from a specific memory location into the accumulator. |
| `STORE` | `21` | Store a word from the accumulator into a specific memory location. |
| `ADD` | `30` | Add a word from a specific location in memory to the word in the accumulator. Leave the result in the accumulator. |
| `SUBTRACT` | `31` | Subtract a word from a specific location in memory from the word in the accumulator. Leave the result in the accumulator. |
| `DIVIDE` | `32` | Divide the word in the accumulator by a word from a specific location in memory. Leave the result in the accumulator. |
| `MULTIPLY` | `33` | Multiply a word from a specific location in memory by the word in the accumulator. Leave the result in the accumulator. |
| `BRANCH` | `40` | Branch to a specific location in memory |
| `BRANCHNEG` | `41` | Branch to a specific location in memory if the accumulator is negative. |
| `BRANCHZERO` | `42` | Branch to a specific location in memory if the accumulator is zero. |
| `HALT` | `43` | Stop the program. |