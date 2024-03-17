from stomp import Connection, ConnectionListener
import json
import numpy as np
from scipy.io.wavfile import write


def get_active_mq_connection():
    # Implement connection logic here
    connection = Connection([('localhost', 61613)])
    connection.set_listener('listner', StompListener())
    connection.connect(wait=True)
    connection.subscribe(destination='/topic//data/client', id=1, ack='auto')
    connection.subscribe(destination='/topic//data/beacon/1', id=2, ack='auto')
    connection.subscribe(destination='/topic//data/beacon/2', id=3, ack='auto')
    connection.subscribe(destination='/topic//data/beacon/3', id=4, ack='auto')
    connection.subscribe(destination='/topic//data/beacon/4', id=5, ack='auto')
    connection.subscribe(destination='/topic//data/beacon/5', id=6, ack='auto')
    return connection


BEACON_PRESET = {
    1: {"x": 360, "y": 0},
    2: {"x": 0, "y": 363},
    3: {"x": 360, "y": 363},
    4: {"x": 700, "y": 363},
    5: {"x": 360, "y": 802}
}


class StompListener(ConnectionListener):
    def on_error(self, frame):
        print('Received an error:', frame.body)

    def on_message(self, frame):
        # save message to raw file
        message_data = json.loads(frame.body)
        destination = frame.headers['destination']

        if destination.startswith('/topic//data/beacon/'):
            beacon_number = destination.split('/')[-1]
            try:
                beacon_number = int(beacon_number)
                beacon_location = BEACON_PRESET[beacon_number]
                message_data['position'] = beacon_location

                filename = f"beacon-{beacon_number}"
            except ValueError:
                print("Invalid beacon number in destination:", destination)

        elif destination == '/topic//data/client':
            client_id = message_data.get('id')

            if client_id is not None:
                filename = f"client-{client_id}"
            else:
                print("Message does not contain an 'id' field")

        try:
            with open(filename + ".json", "w") as file:
                file.write(json.dumps(message_data))

            raw_audio = np.array(message_data['raw'], dtype=np.float32)
            sample_rate = 48000
            write(filename + ".wav", sample_rate, raw_audio)
        except NameError:
            print("Filename not defined. Data not stored to file.")
