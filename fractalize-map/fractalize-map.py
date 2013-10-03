import csv, sys, random

SVG_OUT = "out.svg"
random.seed()
CHANGE_SCALE = 0.05 if len(sys.argv) == 1 else float(sys.argv[1])
SUBDIVISIONS = 100 if len(sys.argv) == 1 else int(sys.argv[2])

islands = {
    "main": "main-island.points",
    "left": "left-island.points",
    "bottom-top": "bottom-island-top-half.points",
    "bottom-bottom": "bottom-island-bottom-half.points",
    "top": "top-island.points"
    }

def parse_file(island_name):
    """ Outputs a list of X, Y tuples to be made into a line """

    filename = islands[island_name]
    with open(filename, "r") as f:
        reader = csv.reader(f)
        return [(int(line[0]), int(line[1])) for line in reader]


def fractalize(start_point, end_point, percentage, previous_change, to_change=None):
    """ 
    Changes a point to be off of the main line by a bit. 
    The point it's moving is percentage (for instance, 0.5)
    between start_point and end_point, and is offset in the
    normal direction
    """
    (x1, y1) = start_point
    (x2, y2) = end_point
    

    (x, y) = (x1 + (x2 - x1) * percentage, y1 + (y2 - y1) * percentage)
    
    #slope = (y2 - y1) / float(x2 - x1)
    #slope = dY / dX
    #normal = -dX / dY
    
    normal_x = y2 - y1
    normal_y = - (x2 - x1)
    
    change = previous_change + 2 * (random.random() - 0.5) * CHANGE_SCALE
    change = force_within_range(change, -1.0, 1.0)

    if to_change != None:
        change += (change - to_change) * random.random()  * CHANGE_SCALE * 2

    (x, y) = (x + change * normal_x, y + change * normal_y)
    return (int(x), int(y)), change

def force_within_range(x, minimum, maximum):
    return max(minimum, min(maximum, x))

def fractalize_points(points):
    ret = []
    x_pre, y_pre = None, None
    change = 0
    for i in range(len(points)):
        if i != 0:
            to_change = None if i != len(points) - 1 else 0
            for percentage in xrange(0, SUBDIVISIONS + 1):
                new_point, change = fractalize(points[i-1], points[i], percentage / float(SUBDIVISIONS), change, to_change)
                ret.append(new_point)
    return ret

def get_extreme_values(fun, get_first_value, points):
    return fun((p[0 if get_first_value else 1] for p in points))

def points2polygon(f, points):
    """ 
    Converts a list of X, Y tuples into a line.
    Assumes that the first and last points are supposed to be equal
    Writes to f
    """
    min_x = min((p[0] for p in points))
    max_x = max((p[0] for p in points))

    min_y = min((p[1] for p in points))
    max_y = max((p[1] for p in points))
    
    f.write('<polygon points="' + " ".join([str(p[0]) + "," + str(p[1]) for p in points]) + '"/>')

def world2svg(f):
    points = {}
    for island in islands:
        points[island] = fractalize_points(parse_file(island))
        
    min_x, min_y, max_x, max_y = None, None, None, None

    min_x = get_extreme_values(min, True, sum((points[island] for island in islands), []))
    min_y = get_extreme_values(min, False, sum((points[island] for island in islands), []))
    max_x = get_extreme_values(max, True, sum((points[island] for island in islands), []))
    max_y = get_extreme_values(max, False, sum((points[island] for island in islands), []))

    f.write('<?xml version="1.0"?>')
    f.write('<svg width="%d" height="%d"' % (max_x - min_x, max_y - min_y))
    f.write('  viewBox="%d %d %d %d"' % (min_x, min_y, max_x, max_y))
    f.write('  version="1.1"')
    f.write('  xmlns="http://www.w3.org/2000/svg">')
    
    for island in islands:
        points2polygon(f, points[island])

    f.write('</svg>\n')

with open("out.svg", "w") as f:
    world2svg(f)
