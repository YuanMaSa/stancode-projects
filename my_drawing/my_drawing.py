"""
File: my_drawing.py
Name: Jonathan Ma
----------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GRect, GPolygon, GArc, GLabel, GLine
from campy.graphics.gtypes import GPoint
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked
from campy.graphics.gimage import GImage

# Constants control the diameter of the window
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 700
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title="amusing dinosaur")


def main():
    """
    TODO:
    """
    onmouseclicked(monitor_x_y)
    # add line object
    for i in add_line():
        window.add(i)

    center = GPoint(window.width / 2, window.height / 2)
    radius = 85
    # add flash background
    flash = add_yellow_flash()
    window.add(flash)
    # add polygon object
    for i in add_polygon():
        window.add(i)

    # add rect object
    window.add(add_rect(center, radius))

    # add arc object
    for i in add_arc():
        window.add(i)
    # add oval object
    for i in add_oval(center, radius):
        window.add(i)

    # add head
    head = GArc(2 * radius, 2 * radius, 15, 300, x=center.x - radius, y=center.y - radius - 170)
    head.filled = True
    head.fill_color = "#8eded9"
    window.add(head)

    # add mouth
    mouth = GPolygon()
    mouth_p = [
        {'x': 685, 'y': 164},
        {'x': 681, 'y': 161},
        {'x': 663, 'y': 160},
        {'x': 645, 'y': 163},
        {'x': 628, 'y': 171},
        {'x': 620, 'y': 184},
        {'x': 620, 'y': 199},
        {'x': 625, 'y': 214},
        {'x': 642, 'y': 228},
        {'x': 659, 'y': 235},
        {'x': 675, 'y': 235},
        {'x': 677, 'y': 234},
        {'x': 665, 'y': 223},
        {'x': 655, 'y': 209},
        {'x': 653, 'y': 194},
        {'x': 661, 'y': 177},
        {'x': 670, 'y': 170}
    ]
    for i in mouth_p:
        mouth.add_vertex((i["x"], i["y"]))

    mouth.filled = True
    mouth.fill_color = '#000000'
    window.add(mouth)

    # add eyes
    for items in add_eyes(center, radius):
        window.add(items)

    # add label
    window.add(add_label())
    # add image
    window.add(add_image(), 1000, 300)

def add_eyes(center, radius):
    """
    :param center:
    :param radius:
    :return: eye object
    """
    l_eye = GOval(30, 30, x=center.x - radius + 70, y=center.y-radius - 150)
    l_eye.filled = True
    l_eye.fill_color = "#FFFFFF"

    l_eyeball = GOval(10, 10, x=center.x - radius + 80, y=center.y-radius - 142.5)
    l_eyeball.filled = True
    l_eyeball.fill_color = "#000200"

    r_eye = GOval(30, 30, x=center.x - radius + 100, y=center.y-radius - 150)
    r_eye.filled = True
    r_eye.fill_color = "#FFFFFF"

    r_eyeball = GOval(10, 10, x=center.x - radius + 110, y=center.y-radius - 142.5)
    r_eyeball.filled = True
    r_eyeball.fill_color = "#000200"

    return l_eye, l_eyeball, r_eye, r_eyeball

def add_yellow_flash():
    """

    :return: flash object
    """
    flash_point = [
        {'x': 382, 'y': 85},
        {'x': 496, 'y': 144},
        {'x': 276, 'y': 181},
        {'x': 398, 'y': 252},
        {'x': 271, 'y': 399},
        {'x': 425, 'y': 322},
        {'x': 388, 'y': 477},
        {'x': 590, 'y': 400},
        {'x': 777, 'y': 484},
        {'x': 719, 'y': 387},
        {'x': 887, 'y': 405},
        {'x': 795, 'y': 318},
        {'x': 969, 'y': 304},
        {'x': 819, 'y': 247},
        {'x': 954, 'y': 135},
        {'x': 636, 'y': 116},
        {'x': 637, 'y': 15},
        {'x': 550, 'y': 101}
    ]

    flash = GPolygon()
    for i in flash_point:
        flash.add_vertex((i["x"], i["y"]))
    flash.filled = True
    flash.fill_color = "#fed91e"
    return flash

def add_arc():
    """

    :return: arc object
    """
    l_hand = GArc(200, 200, 60, 150, x=480, y=270)
    l_hand.filled = True
    l_hand.fill_color = "#8eded9"

    r_hand = GArc(200, 200, -30, 120, x=650, y=300)
    r_hand.filled = True
    r_hand.fill_color = "#8eded9"

    return l_hand, r_hand

def add_oval(c, r):
    """

    :param c: center value
    :param r: radius value
    :return: oval object
    """
    body = GOval(200, 250, x=c.x - r - 20, y=240)
    body.filled = True
    body.fill_color = '#8eded9'

    l_leg = GOval(50, 80, x=540, y=450)
    l_leg.filled = True
    l_leg.fill_color = '#8eded9'

    r_leg = GOval(50, 80, x=650, y=450)
    r_leg.filled = True
    r_leg.fill_color = '#8eded9'

    tail = GOval(100, 40, x=450, y=423)
    tail.filled = True
    tail.fill_color = '#8eded9'

    return l_leg, r_leg, tail, body

def add_rect(c, r):
    """

    :param c: center value
    :param r: radius value
    :return: rect object
    """
    body = GRect(50, 200, x=c.x - r + 2, y=200)
    body.filled = True
    body.fill_color = '#8eded9'

    return body


def add_polygon():
    """

    :return: polygon object
    """

    foot1 = GPolygon()
    l_foot = [
        {'x': 561, 'y': 507},
        {'x': 530, 'y': 522},
        {'x': 564, 'y': 531},
        {'x': 558, 'y': 527},
        {'x': 551, 'y': 541},
        {'x': 567, 'y': 529},
        {'x': 570, 'y': 544},
        {'x': 577, 'y': 522}
    ]

    for i in l_foot:
        foot1.add_vertex((i["x"], i["y"]))
    foot1.filled = True
    foot1.fill_color = '#8eded9'

    foot2 = GPolygon()
    r_foot = [
        {'x': 671, 'y': 505},
        {'x': 713, 'y': 523},
        {'x': 673, 'y': 528},
        {'x': 693, 'y': 537},
        {'x': 686, 'y': 527},
        {'x': 676, 'y': 530},
        {'x': 669, 'y': 542},
        {'x': 663, 'y': 524}
    ]
    for i in r_foot:
        foot2.add_vertex((i["x"], i["y"]))

    foot2.filled = True
    foot2.fill_color = '#8eded9'

    nail1 = GPolygon()
    r_nail = [
        {'x': 717, 'y': 392},
        {'x': 716, 'y': 415},
        {'x': 725, 'y': 398},
        {'x': 727, 'y': 419},
        {'x': 733, 'y': 405},
        {'x': 743, 'y': 427},
        {'x': 742, 'y': 412}
    ]
    for i in r_nail:
        nail1.add_vertex((i["x"], i["y"]))

    nail1.filled = True
    nail1.fill_color = '#8eded9'

    nail2 = GPolygon()
    l_nail = [
        {'x': 519, 'y': 363},
        {'x': 518, 'y': 392},
        {'x': 508, 'y': 372},
        {'x': 509, 'y': 394},
        {'x': 499, 'y': 378},
        {'x': 496, 'y': 401},
        {'x': 490, 'y': 383}
    ]
    for i in l_nail:
        nail2.add_vertex((i["x"], i["y"]))

    nail2.filled = True
    nail2.fill_color = '#8eded9'

    tail = GPolygon()
    tail_p = [
        {'x': 527, 'y': 413},
        {'x': 475, 'y': 425},
        {'x': 397, 'y': 404},
        {'x': 454, 'y': 451},
        {'x': 544, 'y': 450}
    ]
    for i in tail_p:
        tail.add_vertex((i["x"], i["y"]))

    tail.filled = True
    tail.fill_color = '#8eded9'

    return foot1, foot2, nail1, nail2, tail

def add_label():
    """

    :return: label object
    """
    label = GLabel("hello", x=1000, y=650)
    label.font = '-40'
    label.text = "I've tried ..."
    label.color = "#4B0082"

    return label

def add_image():
    """

    :return: image object
    """
    img = GImage('dinosaur.png')
    return img

def add_line():
    """

    :return: line object
    """
    hair_1 = GLine(642, 97, 642, 90)
    hair_1.color = '#000000'

    hair_2 = GLine(647, 99, 647, 90)
    hair_2.color = '#000000'

    hair_3 = GLine(654, 101, 657, 95)
    hair_3.color = '#000000'
    return hair_1, hair_2, hair_3

def monitor_x_y(e):
    """

    :param e: event param
    :return: position value in dict
    """
    hole = GOval(10, 10, x=e.x - 10/2, y=e.y - 10/2)

    hole.filled = True
    hole.fill_color = '#000000'
    window.add(hole)

    item = dict()
    item["x"] = e.x
    item["y"] = e.y
    print(item)


if __name__ == '__main__':
    main()
