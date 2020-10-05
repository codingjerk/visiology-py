import pytest
from typing import Callable
from unittest.mock import Mock
from datetime import datetime, timedelta


@pytest.fixture
def emission_date() -> datetime:
    return datetime(2020, 1, 2, 3, 4, 5)


@pytest.fixture
def expires_in() -> timedelta:
    return timedelta(seconds=3600)


@pytest.fixture
def expire_date(
    emission_date: datetime,
    expires_in: timedelta,
) -> datetime:
    return emission_date + expires_in


@pytest.fixture
def before_expire_date(
    emission_date: datetime,
    expires_in: timedelta,
) -> datetime:
    return emission_date + expires_in / 2


@pytest.fixture
def after_expire_date(
    emission_date: datetime,
    expires_in: timedelta,
) -> datetime:
    return emission_date + expires_in * 2


@pytest.fixture
def fixed_datetime() -> Callable[[datetime], Mock]:
    def fixture(fix: datetime) -> Mock:
        mock_datetime = Mock()
        mock_datetime.now = Mock(return_value=fix)

        return mock_datetime

    return fixture
