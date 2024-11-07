class Box:
    __slots__ = ['x', 'y', 'z', 'sizeX', 'sizeY', 'sizeZ', 'weight']

    def __init__(self, x: float, y: float, z: float, sizeX: float, sizeY: float, sizeZ: float, weight: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.weight = weight


class Waypoint:
    __slots__ = ['uuid', 'x', 'y', 'speed']

    def __init__(self, uuid: str, x: float, y: float,  speed: float) -> None:
        self.uuid = uuid
        self.x = x
        self.y = y
        self.speed = speed