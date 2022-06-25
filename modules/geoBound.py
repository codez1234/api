from shapely.geometry import Point


def check_current_lat_lon(current, destination):

    # latitude, longitude
    x = float(10)

    (lat_c, lon_c) = current
    (lat_d, lon_d) = destination
    site = Point(float(lat_d), float(lon_d)).buffer(
        0.005)  # first two decimal place
    # site = Point(float(lat_d), float(lon_d)).buffer(0.0002)
    # print(site.area)
    user_position = Point(float(lat_c), float(lon_c))
    value = site.contains(user_position)  # returns True
    return value


def is_arrived(current, sites_list):
    values = None
    j = 0
    for i in sites_list:
        if check_current_lat_lon(current, i):
            values = j
            break
        j += 1

    return values


# print(is_arrived(current=('22.60125', '88.415646'),
#       sites_list=[('50', '50'), ('22.6014977', '88.4112308')]))
