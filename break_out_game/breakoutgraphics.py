"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.
COLOR_NUM = 5          # Number of colors of bricks
INIT_SCORE = 0         # Initial score

class BreakoutGraphics:

    def __init__(self, game_start=False, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 dy=INITIAL_Y_SPEED, score=INIT_SCORE, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = "#007799"
        self.window.add(self.paddle, (window_width-paddle_width)/2, window_height-paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius)
        self.ball.filled = True
        self.ball.fill_color = "#000000"
        self.window.add(self.ball, window_width/2, window_height/2)

        # Initialize our mouse listeners
        onmouseclicked(self.click_monitor)
        onmousemoved(self.paddle_position_monitor)

        # Draw bricks
        self.red_arr = []
        self.orange_arr = []
        self.yellow_arr = []
        self.green_arr = []
        self.blue_arr = []

        for x in range(0, brick_cols):
            for y in range(0, brick_rows):
                self.current_brick = GRect(brick_width, brick_height)
                self.current_brick.filled = True
                if y < brick_rows//COLOR_NUM:
                    self.current_brick.fill_color = "#CC0000"
                    self.red_arr.append(
                        (x * (brick_width + brick_spacing), brick_offset + y * (brick_height + brick_spacing))
                    )
                elif brick_rows//COLOR_NUM <= y < brick_rows//COLOR_NUM*2:
                    self.current_brick.fill_color = "#FFAA33"
                    self.orange_arr.append(
                        (x * (brick_width + brick_spacing), brick_offset + y * (brick_height + brick_spacing))
                    )
                elif brick_rows//COLOR_NUM*2 <= y < brick_rows//COLOR_NUM*3:
                    self.current_brick.fill_color = "#FFFF00"
                    self.yellow_arr.append(
                        (x * (brick_width + brick_spacing), brick_offset + y * (brick_height + brick_spacing))
                    )
                elif brick_rows//COLOR_NUM*3 <= y < brick_rows//COLOR_NUM*4:
                    self.current_brick.fill_color = "#227700"
                    self.green_arr.append(
                        (x * (brick_width + brick_spacing), brick_offset + y * (brick_height + brick_spacing))
                    )
                elif brick_rows//COLOR_NUM*4 <= y < brick_rows:
                    self.current_brick.fill_color = "#0000FF"
                    self.blue_arr.append(
                        (x * (brick_width + brick_spacing), brick_offset + y * (brick_height + brick_spacing))
                    )
                self.window.add(
                    self.current_brick,
                    x*(brick_width+brick_spacing),
                    brick_offset+y*(brick_height+brick_spacing)
                )

        self.brick_point_arr = self.red_arr + self.orange_arr + self.yellow_arr + self.green_arr + self.blue_arr
        self.brick_num = len(self.brick_point_arr)

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = dy
        if random.random() > 0.5:
            self.__dx = - self.__dx

        # set up game_start param, initial hint, count down label, show adding score display
        self.game_start = game_start
        self.initial_hint = GLabel('tap to start')
        self.window.add(
            self.initial_hint,
            self.window.width / 2 + BRICK_SPACING - BRICK_WIDTH,
            self.window.height / 2 - 2 * BRICK_SPACING
        )
        self.count_down_label = GLabel('3')
        self.count_down_label.font = '-20'
        self.adding_score_display = GLabel('')
        self.adding_score_display.font = '-20'
        self.adding_score_display.color = '#0000CC'

        # set up score display
        self.player_score = score
        self.score_display = GLabel(f'Score: {self.player_score}')
        self.score_display.font = "-20"
        self.window.add(
            self.score_display,
            0,
            self.window.height - brick_spacing
        )

        # set up lives display
        self.first_lives = GImage('heart.png')
        self.second_lives = GImage('heart.png')
        self.third_lives = GImage('heart.png')
        self.window.add(self.first_lives, self.window.width-brick_width, self.window.height-2*brick_height)
        self.window.add(self.second_lives, self.window.width - 2*brick_width, self.window.height - 2 * brick_height)
        self.window.add(self.third_lives, self.window.width - 3*brick_width, self.window.height - 2 * brick_height)

        # set up event exception object checklist
        self.anti_animation = [
            self.score_display, self.first_lives, self.second_lives, self.third_lives, self.adding_score_display
        ]

    def get_vx(self):
        """

        :return: x speed
        """
        return self.__dx

    def set_vx(self, new_dx):
        """

        :return: None
        """
        self.__dx = new_dx

    def get_vy(self):
        """

        :return: y speed
        """
        return self.__dy

    def set_vy(self, new_vy):
        """

        :param new_vy:
        :return: None
        """
        self.__dy = new_vy

    def get_ball_info(self):
        """

        :return: ball info => x, y, width, height
        """
        return {
            "x": self.ball.x,
            "y": self.ball.y,
            "width": self.ball.width,
            "height": self.ball.height
        }

    def set_ball_position(self, new_x_position, new_y_position):
        """

        :return: None
        """
        self.ball.x = new_x_position
        self.ball.y = new_y_position

    def paddle_position_monitor(self, e):
        """

        :param e:
        :return: None
        """
        if e.x >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
            print(self.paddle.x)
        elif e.x <= 0:
            self.paddle.x = 0
        else:
            self.paddle.x = e.x

        self.window.add(self.paddle, x=self.paddle.x, y=self.paddle.y)

    def click_monitor(self, e):
        """

        :return: None
        """
        self.window.remove(self.initial_hint)
        self.game_start = True

    def ball_moving_event_handler(self):
        """

        :return: object or []
        """
        point1_obj = self.window.get_object_at(self.ball.x, self.ball.y)  # up left
        point2_obj = self.window.get_object_at(self.ball.x+2*BALL_RADIUS, self.ball.y)  # up right
        point3_obj = self.window.get_object_at(self.ball.x, self.ball.y+2*BALL_RADIUS)   # down left
        point4_obj = self.window.get_object_at(self.ball.x+2*BALL_RADIUS, self.ball.y+2*BALL_RADIUS)  # down right

        p1 = None
        p2 = None
        p3 = None
        p4 = None

        if point1_obj is not None:
            # up left event
            p1 = point1_obj
            return [p1]
        elif point2_obj is not None:
            # up right event
            p2 = point2_obj
            return [p2]
        elif point3_obj is not None:
            # down left event
            p3 = point3_obj
            return [p3]
        elif point4_obj is not None:
            # down right event
            p4 = point4_obj
            return [p4]

        if p1 is None and p2 is None and p3 is None and p4 is None:
            return []
        # print("none of hit event")
        return [p1, p2, p3, p4]

    def brick_removal(self, item):
        """

        :param item: GRect object
        :return: None
        """
        point = 0
        color = ''

        if (item.x, item.y) in self.red_arr:
            # red point for 1000
            point = 1000
            color = "#CC0000"
        elif (item.x, item.y) in self.orange_arr:
            # orange point for 800
            point = 800
            color = "#FFAA33"
        elif (item.x, item.y) in self.yellow_arr:
            # yellow point for 600
            point = 600
            color = "#FFFF00"
        elif (item.x, item.y) in self.green_arr:
            # green point for 400
            point = 400
            color = "#227700"
        elif (item.x, item.y) in self.blue_arr:
            # blue point for 200
            point = 200
            color = "#0000FF"
        self.window.remove(item)
        self.set_score_label(point)
        self.show_adding_point(point, color, show=True)

    def set_score_label(self, adding_score):
        """

        :param adding_score:
        :return: None
        """
        self.player_score += adding_score
        self.score_display.text = f'Score: {self.player_score}'

    def check_lives(self, num):
        if num == 2:
            self.window.remove(self.first_lives)
        elif num == 1:
            self.window.remove(self.second_lives)
        elif num == 0:
            self.window.remove(self.third_lives)
            self.check_result()

    def check_result(self, lose=True):
        """

        :param lose:
        :return: None
        """
        res_font = GLabel('')
        if lose:
            self.window.remove(self.ball)
            self.window.add(GImage('drake.jpeg'), self.window.width/2 - 2*BRICK_WIDTH, self.window.height/2)
            res_font.text = 'You lose!'
        else:
            res_font.text = 'You win!'
        res_font.font = "-30"
        res_font.color = "#880000"

        self.window.add(
            res_font,
            self.window.width / 2 - BRICK_WIDTH - 2 * BRICK_SPACING,
            self.window.height / 2
        )

    def count_down_handler(self, time):
        if time == 3:
            self.window.add(
                self.count_down_label,
                self.window.width / 2,
                self.window.height / 2 - 2 * BRICK_SPACING
            )
        if time == 2:
            self.count_down_label.text = "2"
        elif time == 1:
            self.count_down_label.text = "1"
        elif time == 0:
            self.window.remove(self.count_down_label)
            self.count_down_label.text = "3"

    def show_adding_point(self, point, color, show=False):
        """

        :param point:
        :param color:
        :param show:
        :return: None
        """

        if show is True:
            self.adding_score_display.text = f'+{point}'
            self.adding_score_display.color = color
            self.window.add(
                self.adding_score_display,
                0,
                self.window.height - 15 * BRICK_SPACING
            )

        if point == 0 and show is False:
            self.window.remove(self.adding_score_display)

