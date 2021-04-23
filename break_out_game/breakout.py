"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    usr_lives = NUM_LIVES
    graphics = BreakoutGraphics()
    brick_num = graphics.brick_num

    while graphics.game_start is False:
        pause(FRAME_RATE)
        pause(400)
        graphics.window.remove(graphics.initial_hint)
        pause(400)
        graphics.window.add(graphics.initial_hint)
        if graphics.game_start is True:
            graphics.window.remove(graphics.initial_hint)
            break
    # wait til count down
    count_down_event(graphics)
    # Add animation loop here!
    while True:
        graphics.game_start = False
        cur_x_speed = graphics.get_vx()
        cur_y_speed = graphics.get_vy()

        # update
        graphics.ball.move(cur_x_speed, cur_y_speed)

        # check
        check_obj = graphics.ball_moving_event_handler()
        if len(check_obj) > 0:
            # check the event related to four points of the ball
            for item in check_obj:
                if item not in graphics.anti_animation:
                    if item is not None and item is graphics.paddle:
                        # paddle hit event
                        graphics.ball.y = graphics.get_ball_info()["y"] - 25
                        graphics.set_vy(cur_y_speed*-1)
                    elif item is not None and item is not graphics.paddle:
                        # brick hit event
                        graphics.set_vy(cur_y_speed*-1)
                        graphics.brick_removal(item)
                        brick_num -= 1
                        point_adding_event(graphics)
        else:
            ball_info = graphics.get_ball_info()
            if ball_info["x"] <= 0 or ball_info["x"] + ball_info["width"] >= graphics.window.width:
                # when ball is outer x-axis
                graphics.set_vx(cur_x_speed*-1)

            if ball_info["y"] <= 0:
                # when ball is outer y-axis
                graphics.set_vy(cur_y_speed*-1)

        if graphics.ball.y + graphics.ball.height > graphics.window.height:
            # lose event
            usr_lives -= 1
            graphics.check_lives(usr_lives)
            graphics.set_ball_position(graphics.window.width/2, graphics.window.height/2)
            if 0 < usr_lives < 3:
                count_down_event(graphics)

        # pause
        pause(FRAME_RATE)

        # break status
        if brick_num == 0:
            graphics.check_result(lose=False)
        if usr_lives == 0 or brick_num == 0:
            break

def count_down_event(obj):
    """

    :param obj:
    :return: None
    """
    obj.count_down_handler(3)
    pause(800)
    obj.count_down_handler(2)
    pause(800)
    obj.count_down_handler(1)
    pause(800)
    obj.count_down_handler(0)

def point_adding_event(obj):
    """

    :param obj:
    :return: None
    """
    pause(20)
    obj.show_adding_point(0, '', show=False)


if __name__ == '__main__':
    main()
