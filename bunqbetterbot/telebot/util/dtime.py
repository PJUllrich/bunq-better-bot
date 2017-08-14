from datetime import datetime, timezone


def get_early_midnight(date: datetime):
    """
    Sets the time of a datetime object to the earliest possible time (i.e.
    00:00:00.1) of the date of the datetime object. Also sets the timezone
    information of a datetime object to timezone.utc

    Args:
        date: datetime with or without timezone.utc information

    Returns:
        datetime object with the same date, but time set to the earliest time
        of that date (i.e. 00:00:00.1) and with UTC timezone info
    """
    return date.replace(hour=0, minute=0, second=0,
                        microsecond=1, tzinfo=timezone.utc)


def get_late_midnight(date: datetime):
    """
    Same as get_early_midnight only that the time of the datetime object is
    set to the latest possible time (i.e. 23:59:59.999999) of the date of the
    datetime.

    Args:
        date: datetime with or without timezone.utc information

    Returns:
        datetime object with the same date, but time set to the latest time
        of that date (i.e. 23:59:59.999999) and with UTC timezone info
    """
    return date.replace(hour=23, minute=59, second=59,
                        microsecond=999999, tzinfo=timezone.utc)
