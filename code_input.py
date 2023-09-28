import json


def user_instructions(code, forbidden):
    """
    Function checking, executing user input code and handling errors.

    Args:
        code: str containing code performed by user,
        forbidden: list (refers to instructions denied in the current level).
    Returns: Buffer text or error.
    Raises: Environment error if forbidden code is detected.
    """

    # check for unsafe or context-forbidden instructions in code

    with open("assets/text/config/unsafe_words.json", "r") as unsafe_json:
        unsafe = json.loads(unsafe_json.read())     # load from json unsafe words

    forbidden += unsafe

    for word in forbidden:
        if word in code:
            return f"Unsafe instruction ('{word}') found in code input by user."

    # artificial buffer + code modification

    artificial_buffer = ""
    code = code.replace('print(', 'artificial_buffer += (')

    # defining locals dictionary passed into exec, so that variables are affected in the function scope

    local_variables = locals()

    # execution

    try:
        exec(code, globals(), local_variables)
        artificial_buffer = local_variables['artificial_buffer']

    # handling errors

    except Exception as error:
        with open("assets/text/errors.json") as custom_errors_json:
            custom_errors = json.loads(custom_errors_json.read())
            return f'/!\\ {error.__class__.__name__} : {custom_errors[error.__class__.__name__]}'

    return artificial_buffer


res = user_instructions('print("hello world!")', [])
print(res)
