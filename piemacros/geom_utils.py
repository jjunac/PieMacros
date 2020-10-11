from math import cos, degrees, atan2

class GeomUtils:
    @staticmethod
    def coor_to_angle(coor, center):
        return atan2(coor[1] - center[1], coor[0] - center[0])

    @staticmethod
    def are_polar_coor_inside_circle(x_distance_to_center, angle, radius):
        return abs(x_distance_to_center) < abs(cos(angle) * radius)

    @staticmethod
    def current_circle_subdivision(curr_angle, total):
        # TODO: clean this
        return int(((degrees(curr_angle) + 90) / (360/total) + total) % total)


