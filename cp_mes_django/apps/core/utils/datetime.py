"""
DateTime utility functions.
"""

from datetime import datetime, timedelta, date, time
from django.utils import timezone
from django.utils.timezone import make_aware, make_naive
import re


def now() -> datetime:
    """
    Get current datetime with timezone.
    """
    return timezone.now()


def today() -> date:
    """
    Get current date.
    """
    return timezone.now().date()


def to_datetime(value, fmt='%Y-%m-%d %H:%M:%S') -> datetime:
    """
    Convert string to datetime.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, fmt)
    raise ValueError(f'Cannot convert {type(value)} to datetime')


def to_date(value, fmt='%Y-%m-%d') -> date:
    """
    Convert string to date.
    """
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, fmt).date()
    raise ValueError(f'Cannot convert {type(value)} to date')


def format_datetime(dt: datetime, fmt='%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime to string.
    """
    if dt is None:
        return ''
    if timezone.is_aware(dt):
        dt = make_naive(dt)
    return dt.strftime(fmt)


def format_date(d: date, fmt='%Y-%m-%d') -> str:
    """
    Format date to string.
    """
    if d is None:
        return ''
    return d.strftime(fmt)


def parse_datetime_string(value: str) -> datetime:
    """
    Parse datetime string with multiple format support.
    """
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    
    raise ValueError(f'Cannot parse datetime: {value}')


def get_date_range(start_date, end_date) -> list:
    """
    Get list of dates between start and end.
    """
    if isinstance(start_date, str):
        start_date = to_date(start_date)
    if isinstance(end_date, str):
        end_date = to_date(end_date)
    
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    
    return dates


def get_week_range(d: date = None) -> tuple:
    """
    Get start and end date of the week containing the given date.
    """
    if d is None:
        d = today()
    
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    
    return start, end


def get_month_range(d: date = None) -> tuple:
    """
    Get start and end date of the month containing the given date.
    """
    if d is None:
        d = today()
    
    start = d.replace(day=1)
    if d.month == 12:
        end = d.replace(year=d.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end = d.replace(month=d.month + 1, day=1) - timedelta(days=1)
    
    return start, end


def is_workday(d: date) -> bool:
    """
    Check if a date is a workday (Monday to Friday).
    """
    return d.weekday() < 5


def get_workdays_between(start_date, end_date) -> int:
    """
    Count workdays between two dates.
    """
    if isinstance(start_date, str):
        start_date = to_date(start_date)
    if isinstance(end_date, str):
        end_date = to_date(end_date)
    
    count = 0
    current = start_date
    while current <= end_date:
        if is_workday(current):
            count += 1
        current += timedelta(days=1)
    
    return count
