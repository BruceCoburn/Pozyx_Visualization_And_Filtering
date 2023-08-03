def nice_print(string_to_print):
    """
    Prints a string with a border of '*' characters.
    """
    str_len = len(string_to_print)
    print("*" * (str_len + 4))
    print(f"* {string_to_print} *")
    print("*" * (str_len + 4))
