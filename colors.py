import ctypes
import os

COLORS_ENABLED = True

# Enable colors on windows command prompt
if os.name == 'nt' and COLORS_ENABLED:
    kernel32 = ctypes.windll.kernel32
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(hStdOut, mode)


def red(text):
    return "\033[31m" + text + "\033[0m" if COLORS_ENABLED else text


def orange(text):
    return "\033[38;5;172m" + text + "\033[0m" if COLORS_ENABLED else text


def bold_orange(text):
    return "\033[38;5;172;1m" + text + "\033[0m" if COLORS_ENABLED else text


def yellow(text):
    return "\033[38;5;226m" + text + "\033[0m" if COLORS_ENABLED else text


def bold_yellow(text):
    return "\033[38;5;226;1m" + text + "\033[0m" if COLORS_ENABLED else text


def bold_green(text):
    return "\033[38;5;28;1m" + text + "\033[0m" if COLORS_ENABLED else text


def blue(text):
    return "\033[38;5;33m" + text + "\033[0m" if COLORS_ENABLED else text


def bold_blue(text):
    return "\033[38;5;33;1m" + text + "\033[0m" if COLORS_ENABLED else text

