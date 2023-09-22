# wip - code input file

def user_instructions(code, forbidden):
    """
    Function checking, executing user input code and handling errors.

    Args: code:str, forbidden:list (refers to instructions denied in the current level).
    Returns: True if success, Simplified error string else.
    Raises: Environment error if forbidden code is detected.
    """

    # check for unsafe or context-forbidden instructions in code

    unsafe = ["exit", "def"]     # TODO fill this list

    forbidden += unsafe

    for word in forbidden:
        if word in code:
            raise(EnvironmentError, "Unsafe instruction found in code input by user.")

    # artificial buffer + code modification

    artificial_buffer = ""
    code = code.replace('print(', 'artificial_buffer += (')
    code += "print(artificial_buffer)"
    print(code)

    # execution

    try:
        exec(code)
        #global a
        #a = 0
        #resultat = exec("a = 2 \nprint(a)")
        #print(resultat)


    # handling errors
    except Exception as error:
        errors = {"IndexError": "IndexError : L’indice spécifié ([nom de la variable]) = [index qui pose pb] est hors tu tableau !"}     # TODO fill this and export to external json/file
        return errors[error.__class__.__name__]

    return artificial_buffer


res = user_instructions("artificial_buffer = '' \ntab = ['michel berger'] \nfor i in range(1,10):\n  print(tab[0])\n", [])
print(res)
