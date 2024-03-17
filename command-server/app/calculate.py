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


# by using "def", function executes in different thread(worker thread) apart from main thread
# don't use async def
@router.get("/beepbeep")
def calculate_distances(eng=Depends(get_matlab_engine)):
    tf = eng.isprime(37)

    return tf
