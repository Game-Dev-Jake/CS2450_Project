# CS2450_Project

## Prerequisites

To run this program, python 3.10 or later is required.
No additional libraries are required.

## How to Use

Using a command line interface, navigate to the project folder and execute 'python main.py' or 'python3 main.py'
- OR -
Using a code editing software capable of running python such as vscode, run main.py

Upon running main.py, UVSim will automatically initialize a CPU, a 100 word memory, and an accumulator. 

A UI dialogue box will be presented with the following features:

File Header with the following dropdown options:

    - Load File : Upon selection, the user will be presented with a standard OS-dependent load file dialogue box. When a proper file has been selected, the system will automatically import all BasicML lines into memory.

    - Reset Program : Upon selection, the program will remove all text located in the main console, reset each address in memory to the default value of 0000, and reset the accumulator to the default value of 0000.

    - Logs : Upon selection, the user will be presented with a scrollable dialogue box containing program and error logs.

    - Exit : Upon selection, the program will terminate.

Control Button Collection:

    - Run : The program will execute starting at the current address until a HALT command is found or an empty register(0000).

    - Stop : The program will halt execution. NOTE, this is for future use cases. Right now it will stop execution of the program, however the only case where this would be relevant would be during infinite loops where the program will automatically terminate after 1000 passes.

    - Step : The program will execute a single instruction at the current address in memory.

    - Clear Memory : The program will reset each address in memory to the default value of 0000.

    - Clear Accumulator : The program will reset the accumulator to the default value of 0000.

Status Indicator : Indicates the state of execution between running and stopped. NOTE: Currently will only display stopped as the program will either instantly finish or terminate after 1000 passes.

Main Console : Displays all write instruction output.

Memory Display : Displays each memory address in a table format with two columns. The lefthand column contains the memory address, and the righthand column displays the value contained in that address.


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

## Valid BasicML Structure

BasicML files must contain no more than a '+' or '-' followed by a single 4 digit word per line.
For example:
+1009
+1103
-4000
+0000