"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    x_coordinate = int(GRAPH_MARGIN_SIZE+((width-2*GRAPH_MARGIN_SIZE)/len(YEARS))*year_index)
    return x_coordinate

def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################

    # create the line at the top
    canvas.create_line(
        GRAPH_MARGIN_SIZE,
        GRAPH_MARGIN_SIZE,
        CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
        GRAPH_MARGIN_SIZE
    )
    # create the line at the bottom
    canvas.create_line(
        GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
        CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    )

    for i, element in enumerate(YEARS):
        x_axis = get_x_coordinate(CANVAS_WIDTH, i)
        # create vertical lines
        canvas.create_line(
            x_axis,
            GRAPH_MARGIN_SIZE,
            x_axis,
            CANVAS_HEIGHT
        )
        # display the text of years
        canvas.create_text(
            x_axis+TEXT_DX,
            CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
            text=str(YEARS[i]),
            anchor=tkinter.NW,
            font='times 16 bold italic'
        )


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    frame_ratio_y = CANVAS_HEIGHT / MAX_RANK

    for name in lookup_names:
        # data of each baby name
        ranking_info = name_data[name]
        # original queue with year [year, ]
        year_queue = [year for year, ranking in ranking_info.items()]
        # original queue with year and ranking -> [(year, ranking), ]
        processing_queue = [(year, ranking) for year, ranking in ranking_info.items()]

        for year in YEARS:
            if str(year) not in year_queue:
                # assign 1000 <MAX_RANK> to the data which year is not in the queue
                processing_queue.append((str(year), str(MAX_RANK)))
        # recreate an ordered queue -> from 1900 to 2010
        processing_queue = sorted(processing_queue, key=lambda x: int(x[0]))
        print(processing_queue)
        # set up color display
        color_index = get_color_index(lookup_names.index(name), COLORS)

        for i, element in enumerate(processing_queue):
            year_value = int(element[0])
            ranking = int(element[1])
            # set up position for current year data
            x_line_point_1 = get_x_coordinate(CANVAS_WIDTH, YEARS.index(year_value))

            if is_index_out(i, processing_queue):
                # loop through the first point to the point before last point
                x_line_point_2 = get_x_coordinate(CANVAS_WIDTH, (YEARS.index(year_value) + 1))
                next_point_ranking = int(processing_queue[i+1][1])
                res = check_y_position(
                    ranking,
                    MAX_RANK,
                    frame_ratio_y,
                    name,
                    rank_2=next_point_ranking
                )
                y_line_point_1 = res["y1"]
                y_line_point_2 = res["y2"]
                display_text = res["txt"]

                canvas.create_line(
                    x_line_point_1,
                    y_line_point_1,
                    x_line_point_2,
                    y_line_point_2,
                    width=LINE_WIDTH,
                    fill=COLORS[color_index]
                )

            else:
                # loop through the last point
                res = check_y_position(ranking, MAX_RANK, frame_ratio_y, name)
                y_line_point_1 = res["y1"]
                display_text = res["txt"]

            canvas.create_text(
                x_line_point_1 + TEXT_DX,
                y_line_point_1,
                text=display_text,
                anchor=tkinter.SW,
                fill=COLORS[color_index]
            )

def check_y_position(rank_1, max_rank, scale, name, rank_2=0):
    """
    check out the correct position of the y-axis if ranking equals max ranking, then set bottom
    check out the correct text display <name ranking> or <name *>

    :param rank_1: ranking at this point
    :param max_rank: 1000
    :param scale: CANVAS_HEIGHT/MAX_RANK => 600/1000
    :param name: baby name
    :param rank_2: ranking at next point
    :return: a dict with y1 axis, y2 axis and display text
    """
    y_axis_1 = GRAPH_MARGIN_SIZE + (rank_1 * scale)
    y_axis_2 = GRAPH_MARGIN_SIZE + (rank_2 * scale)
    bottom_point = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    txt_display = f"{name} {rank_1}"

    if rank_1 == max_rank:
        y_axis_1 = bottom_point
        txt_display = f"{name} *"

    if rank_2 == max_rank:
        y_axis_2 = bottom_point

    return {
        "y1": y_axis_1,
        "y2": y_axis_2,
        "txt": txt_display
    }

def get_color_index(name_index, color_arr):
    """
    examine color index due to the name index value

    :param name_index: baby name index
    :param color_arr: color array
    :return: color index
    """
    if name_index > len(color_arr):
        color_index = name_index % len(color_arr)
    else:
        color_index = name_index
    return color_index

def is_index_out(index, arr):
    """

    :param index: looping index
    :param arr: array / list
    :return: bool -> if index out of range
    """
    return index < len(arr)-1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
