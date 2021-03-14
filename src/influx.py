#!/usr/bin/python3

from influxdb import InfluxDBClient, exceptions


class Idbc():
    """Class idbc (InfluxDB Client)."""

    def __init__(self, if_db, if_host, if_user, if_pass, if_port=8086):
        """Init idbc class."""
        self.__db = if_db
        self.__client = InfluxDBClient(
            if_host, if_port, if_user, if_pass, if_db)

    def write_data(self, data_points):
        self.last_error = None
        try:
            return self.__client.write_points(data_points)
        except (ConnectionError, ConnectionRefusedError,
                ConnectionAbortedError, ConnectionResetError,
                exceptions.InfluxDBClientError) as e:
            self.last_error = str(e)
            return False

    def purge(self):
        self.last_error = None
        try:
            self.__client.drop_database(self.__db)
            self.__client.create_database(self.__db)
        except (ConnectionError, ConnectionRefusedError,
                ConnectionAbortedError, ConnectionResetError,
                exceptions.InfluxDBClientError) as e:
            self.last_error = str(e)
            return False
