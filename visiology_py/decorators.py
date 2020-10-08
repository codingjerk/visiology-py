import functools
import funcy
import inspect
import json
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Type, TypeVar


Fany = Callable[..., Any]
Decorator = Callable[[Fany], Fany]


def timed(function: Fany) -> Fany:
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        name = function.__name__
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()

        passed = (start_time - end_time) * 1000
        print(f"[{name}]: {passed:.2f} ms")

        return result

    return wrapper


# TODO: create a class instead of function, add idempotent_only mark
# TODO: add idempotent mark to api methods
def cached(time_to_live: timedelta) -> Decorator:
    whitelist = {
        # DC
        "get_dimension_attributes",
        "get_dimension_elements",

        # ViQube
        "version",
    }

    def decorator(function: Fany) -> Fany:
        if function.__name__ not in whitelist:
            return function

        memo: Dict[str, Any] = {}

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = json.dumps([args[1:], kwargs])
            now = datetime.now()

            if key not in memo:
                cached = False
            elif now > memo[key][1] + time_to_live:
                cached = False
            else:
                cached = True

            if cached:
                result, _ = memo[key]
            else:
                result = function(*args, **kwargs)
                memo[key] = result, now

            return result

        return wrapper

    return decorator


# TODO: allow to retry idempotent only or all methods
# TODO: check that max_tries more than zero
# TODO: allow max_tries to be None
def retried(
    max_tries: int,
    timeout_function: Callable[[int], float],
) -> Decorator:
    whitelist = {
        # DC
        "get_dimension_attributes",
        "get_dimension_elements",

        # ViQube
        "version",
    }

    def decorator(function: Fany) -> Fany:
        if function.__name__ not in whitelist:
            return function

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = Exception("Internal error in `retry` decorator")
            for try_number in range(max_tries):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    time.sleep(timeout_function(try_number))
                    last_exception = e

            raise e

        return wrapper

    return decorator


def decorate_api(api: type, *decorators: Decorator) -> None:
    decorator = funcy.compose(*decorators)

    methods = inspect.getmembers(api, predicate=inspect.isfunction)
    for name, method in methods:
        setattr(api, name, decorator(method))
