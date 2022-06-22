import pyautogui
from scipy.spatial import distance
from functools import partial

import time
import sys
from datetime import datetime


def distance_of_mouse_from(x, y):
    actual_pos = pyautogui.position()
    return distance.euclidean((x, y), (actual_pos.x, actual_pos.y))


def _progressBar(
    iterable, prefix="", suffix="", decimals=1, length=100, fill="█", printEnd="\r"
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def do_loopstuff():  # called from loop to move mouse etc.
    pyautogui.moveTo(50, i * 4)
    pyautogui.press("shift")
    return (50, i * 4)


progressBar = partial(_progressBar, prefix="> Moving:", suffix="Complete", length=50)

pyautogui.FAILSAFE = False
numMin = 3
sleepDURATION = 60
TOLERANCE = 55

print(">> Time between moves:", numMin)
print("\n>> Note: Move mouse away from top-left to skip move")

pyautogui.moveTo(1, 1)
last_position = (1, 1)
origin = (0, 0)
position_before_sleep = (0, 0)

while True:
    if (
        distance_of_mouse_from(*origin) < TOLERANCE
        or distance_of_mouse_from(*last_position) < TOLERANCE
        or distance_of_mouse_from(*position_before_sleep) == 0
    ):
        print()
        for i in progressBar(range(0, 200)):
            last_position = do_loopstuff()

            if (
                distance_of_mouse_from(*origin) > TOLERANCE
                and distance_of_mouse_from(*last_position) > TOLERANCE
            ):
                print("> ### breaking current move ###    ")
                break
        print("> Move completed at {}".format(datetime.now().time()))

    # buffer
    time.sleep(3)

    position_before_sleep = (pyautogui.position().x, pyautogui.position().y)
    for x in range(numMin):
        time.sleep(sleepDURATION)
