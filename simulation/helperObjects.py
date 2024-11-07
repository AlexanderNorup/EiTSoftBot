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
    __slots__ = ['id', 'name', 'x', 'y', 'rotation', 'speed']

    def __init__(self, id: str, name: str, x: float, y: float, rotation: float, speed: float) -> None:
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = speed