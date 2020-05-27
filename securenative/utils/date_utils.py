from datetime import datetime


class DateUtils(object):

    @staticmethod
    def to_timestamp(date):
        if not date:
            return datetime.now().strftime("%Y-%d-%dT%H:%M:%S.%fZ")
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
