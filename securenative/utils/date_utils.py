from datetime import datetime


class DateUtils(object):

    @staticmethod
    def to_timestamp(date):
        if not date:
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
