from datetime import datetime


class DateUtils(object):

    @staticmethod
    def to_timestamp(date):
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
