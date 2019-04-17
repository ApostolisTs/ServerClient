from multiprocessing import Lock


class Flight(object):
    """ Flight object. Will be used to store flights and keep them organised. """

    def __init__(self, code, status, time):
        self.code = code
        self.status = status
        self.time = time

    def __repr__(self):
        return f'Flight code: {self.code}, Status: {self.status}, Time: {self.time}'
