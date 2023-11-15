import json

# used in exec(), do not remove
from user_functions import place_block
from user_functions import is_empty


def user_instructions(game, code, forbidden=[]):
    """
    Function checking, executing user input code and handling errors.

    Args:
        game : Game object that can be called inside the exec function to be modified (adding blocks)
        code: str containing code performed by user,
        forbidden: list (refers to instructions denied in the current level).
    Returns: Buffer text or error.
    Raises: Environment error if forbidden code is detected.
    """

    # check for unsafe or context-forbidden instructions in code

    if code.count("\n") > game.level_data["max_lines"] or game.level_data["max_lines"] == 0:
        return f"/!\\ Erreur : le nombre maximum de lignes de code dans ce niveau est {game.level_data['max_lines']}."

    with open("assets/text/unsafe_words.json", "r") as unsafe_json:
        unsafe = json.loads(unsafe_json.read())  # load from json unsafe words

    forbidden += unsafe

    for word in forbidden:
        if word in code:
            return f"Unsafe instruction ('{word}') found in code input by user."

    # artificial buffer + code modification

    artificial_buffer = ""
    code = code.replace('print(', "artificial_buffer +=  '\\n' + str(")
    code = code.replace('place_block(', 'place_block(game,')
    code = code.replace('is_empty(', 'is_empty(game,')

    # defining locals dictionary passed into exec, so that variables are affected in the function scope

    local_variables = locals()

    # execution

    try:
        game.setup()
        exec(code, globals(), local_variables)
        artificial_buffer = local_variables['artificial_buffer']

    # handling errors

    except Exception as error:
        with open("assets/text/errors.json") as custom_errors_json:
            custom_errors = json.loads(custom_errors_json.read())
            try :
                return f'/!\\ {error.__class__.__name__} : {custom_errors[error.__class__.__name__]}\nDebug : {error}'
            except KeyError:
                return str(error)

    return artificial_buffer
