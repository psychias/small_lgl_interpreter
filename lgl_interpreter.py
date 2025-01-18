import sys
import json
from datetime import datetime
import time
import random

global_id_set = set() # initializing global id set used in fancy_id_generator
log = ["id,timestamp,function_name,event"] # initializing log

def fancy_id_generator(global_id_set):
    new_function_id = random.randint(100000, 999999)
    if new_function_id in global_id_set:
        return fancy_id_generator(global_id_set) # Recursive call if if is in global_id_set
    else:
        global_id_set.add(new_function_id)
        return new_function_id

def logger(func):
    def _inner(*args):
        function_name = args[-1][0] # extracting name of called function
        function_id = fancy_id_generator(global_id_set) # using the id generator
        
        message = f"{function_id},{datetime.now()},{function_name},start"
        log.append(message) # saving message to log
        
        time.sleep(0.0001)
        result = func(*args) # calling original func
        time.sleep(0.0001)
        
        message = f"{function_id},{datetime.now()},{function_name},stop"
        log.append(message) # saving message to log
        
        time.sleep(0.0001)
        return result
    return _inner

def do_and(envs_stack, args):
    """
    Handles the 'AND' operation; e.g., [1,"AND",1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to use
        (they can be other operations)

    Returns
    -------
    int
        the logical AND of the two values
    """
    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    assert (left == 0 or left == 1)
    assert (right == 0 or right == 1)

    return int(left) and int(right)

def do_or(envs_stack, args):
    """
    Handles the 'OR' operation; e.g., [1,"OR",1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to use
        (they can be other operations)

    Returns
    -------
    int
        the logical OR of the two values
    """
    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    assert (left == 0 or left == 1)
    assert (right == 0 or right == 1)

    return int(left) or int(right)

def do_xor(envs_stack, args):
    """
    Handles the 'XOR' operation; e.g., [1,"XOR",1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to use
        (they can be other operations)

    Returns
    -------
    int
        the logical XOR of the two values
    """
    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    assert (left == 0 or left == 1)
    assert (right == 0 or right == 1)

    return int(left != right)

def do_add(envs_stack, args):
    """Handles the 'add' operation; e.g., ["add",1,2]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to add
        (they can be other operations)

    Returns
    -------
    int
        the sum of the two values
    """

    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    return left + right


def do_subtract(envs_stack,args):
    """Handles the 'subtract' operation; e.g., ["subtract",1,2]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to subtract

    Returns
    -------
    int
        the difference of the two values
    """

    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    return left - right

def do_multiply(envs_stack,args):
    """Handles the 'multiply' operation; e.g., ["multiply",1,2]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to multiply

    Returns
    -------
    int
        the product of the two values
    """

    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    return left * right


def do_divide(envs_stack,args):
    """Handles the 'divide' operation; e.g., ["divide",1,2]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to divide

    Returns
    -------
    int
        the division of the two values
    """

    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    return left / right



def do_abs(envs_stack, args):
    """Handles the 'abs' operation; e.g., ["abs",-1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : object
        The value for which to compute
        the absolute number

    Returns
    -------
    int
        the absolute number the value
    """

    assert len(args) == 1
    val = do(envs_stack, args[0])
    return abs(val)

def do_seq(envs_stack, args):
    """Handles the 'seq' operation

    Example:
    ["sequence",
        ["set", "alpha", 1],
        ["get", "alpha"]
    ]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of operations to execute

    Returns
    -------
    int
        the return value of the last operation
        in the list of args
    """

    assert len(args) > 0
    result = None
    for expr in args:
        result = do(envs_stack, expr)
    return result

def do_set(envs_stack, args):
    """Handles the 'set' operation; e.g., ["set", "alpha", 1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        where to store/update the variable
    args : list
        args[0] : name of variable
        args[1] : content of variable

    Returns
    -------
    int
        the value associated to the var
    """

    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs_stack, args[1])
    set_in_envs_stack(envs_stack, var_name, value)
    return value


def do_get(envs_stack, args):
    """Handles the 'get' operation; e.g., ["get", "alpha"]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        from which to retrieve the variable
    args : str
        The name of the variable

    Returns
    -------
    object
        the content of the variable
    """

    assert len(args) == 1
    assert isinstance(args[0], str)
    # code below is no longer necessary
    # because the check is done by the function
    # get_from_envs_stack we call later
    # assert args[0] in envs_stack, f"Variable name {args[0]} not found"
    # previous version:
    # value = env[args[0]]
    # new version
    value = get_from_envs_stack(envs_stack, args[0])
    return value


def do_func(envs_stack, args):
    """Handles the 'func' operation; ["func", "n", ["get","n"]]

    This function does not do much: it only
    prepares the data structure to store in
    memory, which can then be called later

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        (only here for consistency)
    args : list
        args[0] : parameters of the function
        args[1] : body of the function

    Returns
    -------
    list
        the list with parameters and body
    """    

    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    return ["func", parameters, body]

@logger
def do_call(envs_stack, args):
    """Handles the 'call' operation; e.g., ["call","add_two",3,2]

    where "add_two" is the name of a function
    previously defined, and the rest are the
    arguments to pass to the function

    Parameters
    ----------
    envs_stack : list
        The stack with the environments,
        to which it pushes the specific env
        for the function when called and
        pop it afterwards
    args : list
        args[0] : name of function to call
        args[1] : arguments to pass to func

    Returns
    -------
    object
        the return value of the body execution
    """
    
    # setting up the call
    assert len(args) >= 1
    assert isinstance(args[0], str)

    func_name = args[0]  # "add_two"
    arguments = [do(envs_stack, a) for a in args[1:]]  # [3, 2]
    
    # find the function
    func = get_from_envs_stack(envs_stack, func_name)
    assert isinstance(func, list) and func[0] == "func", \
            f"{func_name} is not a function!"
    params = func[1]  # ["num1","num2"]
    body = func[2]  # ["addieren","num1","num2"]


    assert len(arguments) == len(params), \
            f"{func_name} receives a different number of parameters"
    # create the env for the function
    # params = ["num1","num2"], values = [3, 2]
    # env = {"num1":3, "num2":2}
    local_env = dict(zip(params, arguments))

    # push new env into the stack
    envs_stack.append(local_env)
    result = do(envs_stack, body)
    envs_stack.pop()
    return result


def set_in_envs_stack(envs_stack, name, value):
    """Adds a variable and its value to the environment stack

    if the variable name has already been defined in the stack of
    environments, it updates the value.
    Otherwise, it creates a new variable in the top environment.

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    name : str
        name of the fuction to set
    value : object
        value to associate to the variable

    Returns
    -------
    None
        nothing is returned, could have returned the set value
    """
    
    assert isinstance(name, str)
    top_environment = envs_stack[-1]
    top_environment[name] = value


def get_from_envs_stack(envs_stack, name):
    """Gets the value of a variable from the environment stack

    It uses lexical scoping: it visits only the first and the last enviroments from the environment stack,
    from the latest inserted environment , to find the variable name.

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    name : str
        name of the value to search

    Returns
    -------
    object
        value to associate to the variable
    """
    assert isinstance(name, str)
    last_env = envs_stack[-1]
    global_env = envs_stack[0]

    if name in last_env:
        return last_env[name]
    if name in global_env:
        return global_env[name]

    # for each_env in reversed(envs_stack):
    #     if name in each_env:
    #         return each_env[name]
    assert False, f"Name {name} not found"


def evaluate_infix(env, expr):

    if isinstance(expr, list):
        if len(expr) == 3 and isinstance(expr[1], str) and expr[1] in OPS:
            left = do(env, expr[0])
            op = expr[1]
            right = do(env, expr[2])

            func = OPS[op]
            return func(env, [left, right])
        
        elif len(expr) > 3 and all(isinstance(expr[i], str) and expr[i] in OPS for i in range(1, len(expr), 2)):
            result = do(env, expr[0])  
            for i in range(1, len(expr) - 1, 2):
                op = expr[i]
                right = do(env, expr[i + 1])

                func = OPS[op]
                result = func(env, [result, right])

            return result

    return expr

def do(env, expr):
    if isinstance(expr, (int, float, dict)):
        return expr
    if isinstance(expr, str):
        if expr == "NULL":
            return None
        return expr
    if expr is None:
        return None

    if isinstance(expr, list) and len(expr) >= 3 and isinstance(expr[1], str) and expr[1] in OPS:
        return evaluate_infix(env, expr)

    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    
    output = func(env, expr[1:])
    return output


# dynamically find and name all operations we support in our language
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}
OPS.update({
    '+':do_add,
    '-':do_subtract,
    '*':do_multiply,
    '/':do_divide,
    'AND': do_and,
    'OR': do_or,
    'XOR': do_xor
    })

def main():
    """
    Executes the interpreter on the given code file.
    Example usage:
    python lgl_interpreter.py example_infix.gsc
    python lgl_interpreter.py example_trace_ours.gsc


    The function also creates the global environment and the stack of
    enviroments, which will be then passed around. It prints the result
    of the computation.
    
    """
    program = ""
    logging_file = None

    if "--trace" in sys.argv:
        assert len(sys.argv) == 4, "incorrect number of system arguments"
        logging_file = sys.argv[3]
    else:
        assert len(sys.argv) == 2, "incorrect number of system arguments"

    with open(sys.argv[1], "r") as source:
        program = json.load(source)
    envs_stack = []  # to be filled with envs
    global_environment = {} # first environment we use
    envs_stack.append(global_environment) # push it to the stack
    result = do(envs_stack, program)
    print(result)
    
    if logging_file: #saving the log into the logging_file passed in the sys args
        with open(logging_file, "w") as log_file:
            for line in log:
                log_file.write(line + "\n")
        

if __name__ == "__main__":
    main()


