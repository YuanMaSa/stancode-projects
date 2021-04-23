"""
File: bouncing_ball.py
Name: Jonathan Ma
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40

window = GWindow(800, 500, title='bouncing_ball.py')

# ball creation
ball = GOval(SIZE, SIZE, x=START_X, y=START_Y)
ball.filled = True
ball.fill_color = "#000000"

# the number of bouncing
bouncing_count = 0
# check if the ball has been clicked
usr_clicked = False
# the number of clicks
count_clicks = 0


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    window.add(ball)
    onmouseclicked(click_event)


def click_event(mouse):
    """
    :param mouse:
    :return: None
    """
    global usr_clicked
    global bouncing_count
    global count_clicks
    vy = 0

    if usr_clicked is False:
        count_clicks += 1
        while True:
            usr_clicked = True
            ball.move(VX, vy)
            if ball.y + ball.height >= window.height:
                # check if the ball hit the ground
                print("hit!!!")
                vy = (-vy + GRAVITY) * REDUCE
                bouncing_count += 1
            else:
                # ball still not reach to the ground
                vy += GRAVITY

            if ball.x + ball.width >= window.width:
                # check if ball move out of the scene
                usr_clicked = False
                break

            print(f"ball position: {ball.y + ball.height}")
            print(f"VY: {str(vy)}")
            pause(DELAY)

        if count_clicks == 3:
            usr_clicked = True

        window.remove(ball)
        window.add(ball, START_X, START_Y)


if __name__ == "__main__":
    main()
