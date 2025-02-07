import platform
import questionary
import re
import sys
from pilot.database.database import save_user_input, get_saved_user_input
from pilot.utils.style import color_yellow_bold, style_config


def remove_ansi_codes(s: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


def styled_select(*args, **kwargs):
    kwargs["style"] = style_config.get_style()
    # TODO add saving and loading of user input
    return questionary.select(*args, **kwargs).unsafe_ask()  # .ask() is included here


def styled_text(project, question, ignore_user_input_count=False, style=None, hint=None):
    if not ignore_user_input_count:
        project.user_inputs_count += 1
        user_input = get_saved_user_input(project, question)
        if user_input is not None and user_input.user_input is not None and project.skip_steps:
            # if we do, use it
            project.checkpoints['last_user_input'] = user_input
            print(color_yellow_bold(f'Restoring user input id {user_input.id}: '), end='')
            print(color_yellow_bold(f'{user_input.user_input}'))
            return user_input.user_input

    if project.check_ipc():
        response = print(question, type='user_input_request')
        print(response)
    else:
        used_style = style if style is not None else style_config.get_style()
        question = remove_ansi_codes(question)  # Colorama and questionary are not compatible and styling doesn't work
        flush_input()
        response = questionary.text(question, style=used_style).unsafe_ask()  # .ask() is included here

    if not ignore_user_input_count:
        save_user_input(project, question, response, hint)

    print('\n\n', end='')
    return response


def get_user_feedback():
    return questionary.text('How did GPT Pilot do? Were you able to create any app that works? '
                            'Please write any feedback you have or just press ENTER to exit: ',
                            style=style_config.get_style()).unsafe_ask()


def ask_user_to_store_init_prompt():
    return questionary.text('We would appreciate if you let us store your initial app prompt. '
                            'If you are OK with that, please just press ENTER',
                            style=style_config.get_style()).unsafe_ask()


def flush_input():
    """Flush the input buffer, discarding all that's in the buffer."""
    try:
        if platform.system() == 'Windows':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except (ImportError, OSError):
        pass
