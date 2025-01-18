[
    "seq",
    ["set", "alpha", [1, "+", [[5, "*", 5], "/", 25]]],
    ["set", "beta", 10],
    ["set", "gamma", ["subtract",19,11]],
    ["set", "multiply_by_five", ["func", "x", ["multiply", ["get", "x"], 5]]],
    ["set", "find_average", ["func", ["a", "b"], ["divide", ["add",["get", "a"], ["get", "b"]],2]]],
    ["call", "find_average", ["call", "multiply_by_five", ["get", "alpha"]],["call", "find_average", ["call", "multiply_by_five", ["get", "gamma"]],["get", "beta"]]]
]