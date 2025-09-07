from enum import Enum

class TransportMode(str, Enum):
    TRUCK = 'truck',
    CAR = 'car',
    BIKE = 'bike'