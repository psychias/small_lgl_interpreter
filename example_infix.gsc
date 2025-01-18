["seq",
    ["set", "alpha", [1, "+", [[5, "*", 5], "/", 25]]],
    ["set", "beta", [["get", "alpha"], "-", 1]],
    ["set", "gamma", 0],
    ["set", "theta", [["get", "beta"], "XOR", ["get", "gamma"]]],
    [1, "AND", [["get", "beta"], "OR", ["get", "gamma"]]]
]