[
    "seq",
    ["set", "x", 100],
    ["set", "one", ["func", "y", ["get", "x"]]],
    ["set", "two", ["func", "y", ["seq", ["set", "x", 42], ["call", "one", "y"]]]],
    ["set", "main", ["func", "y", ["call","two","y"]]],
    ["call","main","y"]
]
