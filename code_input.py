import json
import wrapt_timeout_decorator
import utils

# Might be used in exec(code), do not remove !
from user_functions import place_block
from user_functions import is_empty
from user_functions import frog


def user_instructions(game, code, forbidden=[], timeout=15):
    """
    Function checking, executing user input code and handling errors.

    Args:
        game : Game object that can be called inside the exec function to be modified (adding blocks)
        code: str containing code performed by user,
        forbidden: list (refers to instructions denied in the current level).
        timeout: time limit for the code to run, in seconds. default = 5
    Returns: Buffer text or error.
    Raises: Environment error if forbidden code is detected.
    """

    # check for unsafe or context-forbidden instructions in code

    if code.count("\n") > game.level_data["max_lines"] or game.level_data["max_lines"] == 0:
        return f"/!\\ Error : the maximum of lines of code in this level is {game.level_data['max_lines']}."

    with open("assets/text/unsafe_words.json", "r") as unsafe_json:
        unsafe = json.loads(unsafe_json.read())  # load from json unsafe words

    forbidden += unsafe

    for word in forbidden:
        if word in code:
            return f"/!\\ Error : Forbidden instruction ('{word}') found in code."

    # artificial buffer + code modification

    artificial_buffer = ""
    code = code.replace('print(', "artificial_buffer +=  '\\n' + str(")
    code = code.replace('place_block(', 'place_block(game,')
    code = code.replace('is_empty(', 'is_empty(game,')
    code = code.replace('frog(', 'frog(game,')

    # defining locals dictionary passed into exec, so that variables are affected in the function scope
    local_variables = locals()

    # execution
    try:
        artificial_buffer = code_execution(game, code, globals(), local_variables)

    # handling errors

    except Exception as error:
        print("heuy")
        with open("assets/text/errors.json") as custom_errors_json:
            custom_errors = json.loads(custom_errors_json.read())
            game.setup()
            return f'/!\\ {error.__class__.__name__} : {error}\n{artificial_buffer}'

    return artificial_buffer


@wrapt_timeout_decorator.timeout(5)
# Timeout to prevent from looping infinetly
def code_execution(game, code, global_variables, local_variables):
    """
    Executes the code performed by user. Func used in user_instructions.
    Args:
        game:
        code:
        global_variables:
        local_variables:

    Returns:

    """
    game.setup()
    exec(code, global_variables, local_variables)
    return local_variables['artificial_buffer']