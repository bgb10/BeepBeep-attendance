from stomp import Connection


def get_active_mq_connection():
    # Implement connection logic here
    connection = Connection([('localhost', 61613)])
    connection.connect(wait=True)
    return connection
