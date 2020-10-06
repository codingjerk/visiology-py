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


def cached(time_to_live: timedelta) -> Decorator:
    def decorator(function: Fany) -> Fany:
        has_self = "self" in inspect.signature(function).parameters
        from_arg = 1 if has_self else 0

        memo: Dict[str, Any] = {}

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = json.dumps([args[from_arg:], kwargs])
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


def decorate_api(api: type, *decorators: Decorator) -> None:
    decorator = funcy.compose(decorators)

    methods = inspect.getmembers(api, predicate=inspect.isfunction)
    for name, method in methods:
        if not any([
            name.startswith("get_"),
            name.startswith("post_"),
            name.startswith("put_"),
            name.startswith("delete_"),
        ]):
            continue

        setattr(api, name, decorator(method))
