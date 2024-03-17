from fastapi import APIRouter, Depends
import matlab.engine

router = APIRouter()


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
