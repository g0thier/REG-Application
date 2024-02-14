# Reference :
# https://github.com/antistatique/swisstopo/blob/dev/src/SwisstopoConverter.php

class SwisstopoConverter:
    @staticmethod
    def from_mn95_to_wgs(east, north):
        return {
            'lat': SwisstopoConverter.from_mn95_to_wgs_latitude(east, north),
            'long': SwisstopoConverter.from_mn95_to_wgs_longitude(east, north)
        }

    @staticmethod
    def from_wgs_to_mn95(lat, long):
        return {
            'east': SwisstopoConverter.from_wgs_to_mn95_east(lat, long),
            'north': SwisstopoConverter.from_wgs_to_mn95_north(lat, long)
        }

    @staticmethod
    def from_mn03_to_wgs(y, x):
        return {
            'lat': SwisstopoConverter.from_mn03_to_wgs_latitude(y, x),
            'long': SwisstopoConverter.from_mn03_to_wgs_longitude(y, x)
        }

    @staticmethod
    def from_wgs_to_mn03(lat, long):
        return {
            'x': SwisstopoConverter.from_wgs_to_mn03_x(lat, long),
            'y': SwisstopoConverter.from_wgs_to_mn03_y(lat, long)
        }

    @staticmethod
    def from_mn95_to_wgs_latitude(east, north):
        y_aux = (east - 2600000) / 1000000
        x_aux = (north - 1200000) / 1000000
        lat = 16.9023892 + 3.238272 * x_aux - 0.270978 * y_aux ** 2 - 0.002528 * x_aux ** 2 \
              - 0.0447 * y_aux ** 2 * x_aux - 0.0140 * x_aux ** 3
        lat = lat * 100 / 36
        return lat

    @staticmethod
    def from_mn95_to_wgs_longitude(east, north):
        y_aux = (east - 2600000) / 1000000
        x_aux = (north - 1200000) / 1000000
        long = 2.6779094 + 4.728982 * y_aux + 0.791484 * y_aux * x_aux + 0.1306 * y_aux * x_aux ** 2 \
               - 0.0436 * y_aux ** 3
        long = long * 100 / 36
        return long

    @staticmethod
    def from_mn03_to_wgs_latitude(y, x):
        y_aux = (y - 600000) / 1000000
        x_aux = (x - 200000) / 1000000
        lat = 16.9023892 + 3.238272 * x_aux - 0.270978 * y_aux ** 2 - 0.002528 * x_aux ** 2 \
              - 0.0447 * y_aux ** 2 * x_aux - 0.0140 * x_aux ** 3
        lat = lat * 100 / 36
        return lat

    @staticmethod
    def from_mn03_to_wgs_longitude(y, x):
        y_aux = (y - 600000) / 1000000
        x_aux = (x - 200000) / 1000000
        long = 2.6779094 + 4.728982 * y_aux + 0.791484 * y_aux * x_aux + 0.1306 * y_aux * x_aux ** 2 \
               - 0.0436 * y_aux ** 3
        long = long * 100 / 36
        return long

    @staticmethod
    def from_wgs_to_mn03_y(lat, long):
        lat = SwisstopoConverter.deg_to_sex(lat)
        long = SwisstopoConverter.deg_to_sex(long)
        lat = SwisstopoConverter.deg_to_sec(lat)
        long = SwisstopoConverter.deg_to_sec(long)
        y_aux = (lat - 169028.66) / 10000
        x_aux = (long - 26782.5) / 10000
        return 600072.37 + 211455.93 * x_aux - 10938.51 * x_aux * y_aux - 0.36 * x_aux * y_aux ** 2 \
               - 44.54 * x_aux ** 3

    @staticmethod
    def from_wgs_to_mn03_x(lat, long):
        lat = SwisstopoConverter.deg_to_sex(lat)
        long = SwisstopoConverter.deg_to_sex(long)
        lat = SwisstopoConverter.deg_to_sec(lat)
        long = SwisstopoConverter.deg_to_sec(long)
        y_aux = (lat - 169028.66) / 10000
        x_aux = (long - 26782.5) / 10000
        return 200147.07 + 308807.95 * y_aux + 3745.25 * x_aux ** 2 + 76.63 * y_aux ** 2 \
               - 194.56 * x_aux ** 2 * y_aux + 119.79 * y_aux ** 3

    @staticmethod
    def from_wgs_to_mn95_north(lat, long):
        lat = SwisstopoConverter.deg_to_sex(lat)
        long = SwisstopoConverter.deg_to_sex(long)
        phi = SwisstopoConverter.deg_to_sec(lat)
        lam = SwisstopoConverter.deg_to_sec(long)
        phi_aux = (phi - 169028.66) / 10000
        lam_aux = (lam - 26782.5) / 10000
        return 1200147.07 + 308807.95 * phi_aux + 3745.25 * lam_aux ** 2 + 76.63 * phi_aux ** 2 \
               - 194.56 * lam_aux ** 2 * phi_aux + 119.79 * phi_aux ** 3

    @staticmethod
    def from_wgs_to_mn95_east(lat, long):
        lat = SwisstopoConverter.deg_to_sex(lat)
        long = SwisstopoConverter.deg_to_sex(long)
        phi = SwisstopoConverter.deg_to_sec(lat)
        lam = SwisstopoConverter.deg_to_sec(long)
        phi_aux = (phi - 169028.66) / 10000
        lam_aux = (lam - 26782.5) / 10000
        return 2600072.37 + 211455.93 * lam_aux - 10938.51 * lam_aux * phi_aux - 0.36 * lam_aux * phi_aux ** 2 \
               - 44.54 * lam_aux ** 3

    @staticmethod
    def deg_to_sex(angle):
        deg = int(angle)
        minute = int((angle - deg) * 60)
        second = (((angle - deg) * 60) - minute) * 60
        return deg + minute / 100 + second / 10000

    @staticmethod
    def deg_to_sec(angle):
        deg = int(angle)
        minute = int((angle - deg) * 100)
        second = (((angle - deg) * 100) - minute) * 100
        return second + minute * 60 + deg * 3600
