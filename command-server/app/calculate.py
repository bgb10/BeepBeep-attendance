from fastapi import APIRouter, Depends
import matlab.engine
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()


class Beacon(BaseModel):
    id: int
    x: float
    y: float
    estimatedDistanceToClient: float


class Position(BaseModel):
    x: float
    y: float


class MatlabEngineSingleton:
    """
    FastAPI's dependency injection system does not inherently support the singleton pattern
    Thus, I created a custom singleton class to encapsulate the MATLAB engine initialization logic
    By this, Matlab Engine instance only initiates once at the first injection time.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Initializing MATLAB engine")
            cls._instance = matlab.engine.start_matlab()
        return cls._instance


def get_matlab_engine():
    return MatlabEngineSingleton()


@router.post("/beepbeep")
def calculate_distances(eng=Depends(get_matlab_engine)):
    """
    In FastAPI, "async def" works on Main thread, thus Main thread could be blocked while Matlab is running.
    By using "def", function executes in different thread(worker thread) apart from main thread.
    Thus, main thread not blocks!
    """

    eng.cd('/Users/parkgwanbin/projects/seat-level-attendance-using-beepbeep', nargout=0)
    distance = eng.beepbeepdistance(
        './', 1, nargout=1)

    return distance


@router.post("/triangulation")
def triangulation(beaconList: List[Beacon]):
    """
    With beacon's location and distnance between beacon and client pair,
    we can locate client using triangulation.
    """

    if len(beaconList) < 3:
        raise ValueError("Insufficient data for triangulation")
    elif len(beaconList) > 3:
        print("Use only the first three data!")

    x1, y1 = beaconList[0].x, beaconList[0].y
    x2, y2 = beaconList[1].x, beaconList[1].y
    x3, y3 = beaconList[2].x, beaconList[2].y
    r1, r2, r3 = beaconList[0].estimatedDistanceToClient, beaconList[
        1].estimatedDistanceToClient, beaconList[2].estimatedDistanceToClient

    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

    if (B * D - E * A) == 0:
        raise ValueError("Cannot solve the equations (division by zero)")

    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)

    return x, y


table_coordinates = {
    0: (75, 0),
    1: (75, 128),
    2: (75, 246),
    3: (75, 363),
    4: (75, 473),
    5: (75, 583),
    6: (360, 0),
    7: (360, 128),
    8: (360, 246),
    9: (360, 363),
    10: (360, 473),
    11: (360, 583),
    12: (360, 691),
    13: (360, 802),
    14: (625, 0),
    15: (625, 128),
    16: (625, 246),
    17: (625, 363),
    18: (625, 473),
    19: (625, 583),
    20: (625, 691),
    21: (625, 802)
}


@router.post("/locate")
def locate_client(position: Position):
    closest_table = None
    min_distance = float('inf')

    for table_number, (x, y) in table_coordinates.items():
        distance = ((position.x - x) ** 2 + (position.y - y) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_table = table_number

    return {"answer": closest_table}
