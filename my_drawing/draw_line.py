"""
File: draw_line.py
Name: Jonathan Ma
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GLine
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked

# Constants control the diameter of the window
# WINDOW_WIDTH = 1250
# WINDOW_HEIGHT = 700

# This constant controls the size of the click stroke
SIZE = 20

# Global Variable
window = GWindow()
click_count = 0  # check odd or even type of the click
prev_dot_x = 0  # the x position of prev dot
prev_dot_y = 0  # the y position of prev dot


def main():
    """
    This program creates lines on an instance of GWindow class.
    There is a circle indicating the user’s first click. A line appears
    at the condition where the circle disappears as the user clicks
    on the canvas for the second time.
    """
    onmouseclicked(click_monitoring)
    

def click_monitoring(e):
    """
    monitoring click event
    @input: event body
    @output: None
    """
    global click_count
    global prev_dot_x
    global prev_dot_y

    dot = GOval(SIZE, SIZE, x=e.x - SIZE/2, y=e.y-SIZE/2)
    dot.filled = True
    dot.fill_color = "#00FFFF"

    if click_count % 2 == 0:
        # if check the odd type of the click, then create a dot
        window.add(dot)
    else:
        # if check the even type of the click, then remove prev dot and create a line
        prev_dot = window.get_object_at(prev_dot_x, prev_dot_y)
        window.remove(prev_dot)
        create_line(prev_dot_x, prev_dot_y, e.x, e.y)

    click_count += 1
    prev_dot_x = e.x
    prev_dot_y = e.y

def create_line(x1, y1, x2, y2):
    """
    create a line
    @input: prev_dot x position, prev_dot y position, current x position, current y position 
    @output: None
    """
    line = GLine(x1, y1, x2, y2)
    window.add(line)


if __name__ == "__main__":
    main()