# Extended LGL Interpreter

## Overview

This Python script implements an extended version of the **Little German Language** interpreter, by enabling infix and boolean expressions, as well as lexical scoping and tracing.

## Part 1 Documentation

In this section the infix and boolean operators are explained in detail, which are the extented functions to the original LGL interpreter. All functions described below are implemented within `lgl_interpreter.py`.

## Functions
The infix support for the below Arithmetic and Boolean Operators is enabled by mapping the corresponding arithmetic sign `("+", "-", "*", "/")` or boolean word `("AND", "OR", "XOR")` to the corresponding `do_...()` python function, which is originally implemented in LGL by default. The matching is done through the extension of the OPS dictionary which contains all mappings between the supported operators and their corresponding python functions.

### Arithmetic Operators

`do_add()`

This function implements the arithmetic addition between two inputs which can be any integer between 0 and 9. It supports both prefix and infix usages, as both syntax maps to the same `do_add()` python function in the `OPS` dictionary.

- **Usage:** ["add", 1, 1] or [1, "+", 1]

`do_subtract()`

This function implements the arithmetic subtraction between two inputs which can be any integer between 0 and 9. It supports both prefix and infix usages, as both syntax maps to the same `do_subtract()` python function in the `OPS` dictionary.

- **Usage:** ["subtract", 1, 1] or [1, "-", 1]

`do_multiply()`

This function implements the arithmetic multiplication between two inputs which can be any integer between 0 and 9. It supports both prefix and infix usages, as both syntax maps to the same `do_multiply()` python function in the `OPS` dictionary.

- **Usage:** ["multiply", 1, 1] or [1, "*", 1]

`do_divide()`

This function implements the arithmetic division between two inputs which can be any integer between 0 and 9. It supports both prefix and infix usages, as both syntax maps to the same `do_divide()` python function in the `OPS` dictionary.

- **Usage:** ["divide", 1, 1] or [1, "/", 1]

### Boolean Operators

There are 3 kinds of Boolean operators supported by lgl_interpreter:

`do_and()`

This function implements the logical AND operator between two inputs which can either be 0 or 1. It returns 1 if both inputs are 1, otherwise it returns 0.

- **Usage:** [1, "AND", 1] 

`do_or()`

This function implements the logical OR operator between two inputs which can either be 0 or 1. It returns 1 if the first, the second, or both inputs are 1, otherwise it returns 0.

- **Usage:** [1, "OR", 1] 

`do_xor()`

This function implements the logical XOR operator between two inputs which can either be 0 or 1. It returns 1 if the first and second inputs are different from each other, otherwise it returns 0.

- **Usage:** [1, "XOR", 1] 


## Example Usage

The `lgl_interpreter.py` can be used by running the following command in the Terminal:

```terminal
python lgl_interpreter.py example_infix.gsc
```

The `example_infix.gsc` file contains a sequence of operations which contain all the newly implemented operators which the LDL iterpreter has been expended by: both infix and boolean operators.

The expected result of the sequence presented in `example_infix.gsc` is 0.


## Part 2 Documentation

### Lexical Scoping Implementation

The `interpreter.py` script is designed to support both dynamic and lexical scoping in the LGL interpreter. The script includes a `do_get` function that implements lexical scoping  by searching the environment stack from the most recent environment to the global environment.


## Code Implementation

In `interpreter.py`, lexical scoping is achieved through the `do_get` and `get_from_envs_stack` functions. These functions manage variable retrieval based on the lexical scoping rules:

1. **`get_from_envs_stack(envs_stack, name)`**:
   - This function retrieves the value of a variable by searching through the `envs_stack` in reverse order, starting from the innermost environment.
   - If the variable is not found in the current scope, it continues to search the outer scopes, up to the global environment.

2. **`set_in_envs_stack(envs_stack, name, value)`**:
   - This function sets or updates a variable's value in the appropriate scope, allowing consistent variable bindings across the environment stack.

## Usage

To use the interpreter, run the script from the command line with the following command:

```bash
python lgl_interpreter.py example_scoping.gsc
```



## Part 3 Documentation

3.1 The goal of part 3.1 code is to implement an optional logging system which tracks the usage of user-defined functions in the tll, as well as to save them to a .log file.

`logger`

The `logger` function was created to be a decorator. It is used in front of our `do_call` function to wrap it so that we can track its usage. In `logger` we retrieve the name of the called function through the arguments that are passed into `do_call`. Before and after we actually call the intended function, we construct a log message containing the function_id, timestamp, function_name, and whether it started or stopped.
We pause the function for a very short time in a couple of places to show that the reporting works because otherwise its too quick. After each message is generated it is appended to a global list of messages. At the end of the entire program the list is parsed and saved in the logging file which was passed using the --trace arguement.

`fancy_id_generator`

In `logger` we use the function `fancy_id_generator` to generate unique ids for each user defined function passed into do_call. This id is generated only for the purposes of reporting. The function generates a random 6 digit number, and checks if it has already been used. If so it recursively calls itself again until a number which hasnt been used is found.




### 3.2 Reporting.py

The `reporting.py` script is designed to parse, aggregate, and display function call data from a trace log file, `trace_file.log`. This tool provides a table that includes the function name, the number of times each function was called, the total execution time, and the average execution time.

## Usage

To use the reporting tool, run the script from the command line with the following command:

```bash
python reporting.py trace_file.log
```


## How It Works


1. **Data Parsing (`parse_data` function)**:
    - Reads each line from `trace_file.log`, splits the values by commas, and extracts the `unique_id`, `function_name`, `event` (start or stop), and `timestamp`.
    - Converts each timestamp into a `datetime` object for easier manipulation of time intervals.

2. **Call Stack Analysis (`call_stack` function)**:
    - For each `start` event, it records the start time of the function.
    - For each corresponding `stop` event, it calculates the elapsed time since the last `start`, adds it to `total_time`, increments `calls_counter`, and resets `start_time`.

3. **Table Printing (`print_table` function)**:
    - Prints a formatted table with the following columns:
        - **Function Name**: The name of the function.
        - **Num. of Calls**: Total times the function was called.
        - **Total Time (ms)**: Sum of all execution times in milliseconds.
        - **Average Time (ms)**: Average execution time per call, calculated as `Total Time / Num. of Calls`.


## Example

For a `trace_file.log` file containing:

```plaintext
unique_id,timestamp,function_name,event
1,2024-11-12 10:00:00.000,add_cubes,start
1,2024-11-12 10:00:00.812,add_cubes,stop
2,2024-11-12 10:01:00.000,get_cube_power,start
2,2024-11-12 10:01:00.220,get_cube_power,stop
3,2024-11-12 10:02:00.000,get_cube_power,start
3,2024-11-12 10:02:00.220,get_cube_power,stop
```

The script would output:

```plaintext
| Function Name     | Num. of calls  | Total Time (ms) | Average Time (ms) |
|------------------------------------------------------------------------- |
| add_cubes         | 1              | 0.812           | 0.812             |
| get_cube_power    | 2              | 0.440           | 0.220             |
```


