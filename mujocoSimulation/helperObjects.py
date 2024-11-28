from typing import List

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
    

    def __str__(self):
        return f'Box - ({self.x},{self.y},{self.z}) {self.sizeX}x{self.sizeY}x{self.sizeZ}, {self.weight} kg'


class Waypoint:
    __slots__ = ['id', 'name', 'x', 'y', 'rotation', 'speed']

    def __init__(self, id: str, name: str, x: float, y: float, rotation: float, speed: float) -> None:
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = speed
    

    def __str__(self):
        return f'Waypoint - {self.name}:{self.id} ({self.x},{self.y}) speed:{self.speed} rotation:{self.rotation}'


# in json: Id Name, Waypoints 
class Mission:
    __slots__ = ['id', 'name', 'waypoints']

    def __init__(self, id: str, name: str, waypoints: List[Waypoint]):
        self.id = id
        self.name = name
        self.waypoints = waypoints


    def __str__(self):
        #[f'\n\t{str(waypoint)}' for waypoint in self.waypoints]
        waypoint_strings = ''.join([f'\n\t{str(waypoint)}' for waypoint in self.waypoints])
        return f'Mission - {self.name} {self.id}{waypoint_strings}'



if __name__ == '__main__':
    waypoint = Waypoint(
        '123',
        'somename',
        1,
        1,
        1,
        1
    )
    waypoint1 = Waypoint(
        '312',
        'somename',
        1,
        1,
        1,
        1
    )
    box = Box(
        1,
        1,
        1,
        1,
        1,
        1,
        1
    )
    mission = Mission(
        '123',
        'name',
        [waypoint, waypoint1]
    )
    print(box)
    print(mission)