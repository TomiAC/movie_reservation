import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class Formats(str, enum.Enum):
    TWOD = "2D"
    THREED = "3D"
    FOURD = "4D"
    DOLBY = "DOLBY"
    IMAX = "IMAX"