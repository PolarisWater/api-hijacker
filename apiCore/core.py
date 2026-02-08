from __future__ import annotations
import types

from . import exceptions

import cloudscraper
import requests
import time


class HTTPErrorHandler:
    def __init__(self, accepted=None, terminal=None):
        self.accepted = set(accepted or [200, 201, 204])  # set of accepted status coeds
        self.terminal = set(terminal or [400, 401, 403, 404, 409, 501])  # set of status codes that should not be retried

    def allow(self, status_codes: int | list[int]) -> HTTPErrorHandler:  # add one or multiple status codes that should be accepted
        accepted = set(self.accepted)
        if isinstance(status_codes, int):
            accepted.add(status_codes)
        else:
            accepted.update(status_codes)

        return HTTPErrorHandler(
            accepted=accepted,
            terminal=self.terminal
        )

    def avoid(self, status_codes: int | list[int]) -> HTTPErrorHandler:  # add one or multiple status codes that should be avoided (no retries if received)
        terminal = set(self.terminal)
        if isinstance(status_codes, int):
            terminal.add(status_codes)
        else:
            terminal.update(status_codes)

        return HTTPErrorHandler(
            accepted=self.accepted,
            terminal=terminal
        )

    def __call__(self, func) -> tuple[requests.Response, str]:
        try:
            response: requests.Response = func()  # catch http errors form this function
            if response.status_code in self.accepted:
                return response, 'ok'  # response it accepted

            if response.status_code in self.terminal:
                return response, 'stop'  # stop retries - resending won't help

            return response, 'retry'  # retry on other status codes

        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return requests.Response(), 'retry'  # retry on request exception

        except Exception as e:
            print(f"Exception: {e}")
            return requests.Response(), 'stop'  # stop retries if a non-http error is detected


def getHandle():  # handle must act like requests module
    handle = cloudscraper.create_scraper(
        auto_refresh_on_403=False,
        max_403_retries=0
    )

    handle.headers.update({"Accept-Encoding": "gzip, deflate"})

    return handle


def sendRequest(method: str, url: str, **kwargs) -> requests.Response:
    handle = getHandle()
    try:
        response = handle.request(method, url, **kwargs)
        return response
    finally:
        handle.close()


def get(url: str, **kwargs) -> requests.Response:
    return sendRequest('get', url, **kwargs)


def head(url: str, **kwargs) -> requests.Response:
    return sendRequest('head', url, **kwargs)


def options(url: str, **kwargs) -> requests.Response:
    return sendRequest('options', url, **kwargs)


def put(url: str, **kwargs) -> requests.Response:
    return sendRequest('put', url, **kwargs)


def delete(url: str, **kwargs) -> requests.Response:
    return sendRequest('delete', url, **kwargs)


def post(url: str, **kwargs) -> requests.Response:
    return sendRequest('post', url, **kwargs)


def patch(url: str, **kwargs) -> requests.Response:
    return sendRequest('patch', url, **kwargs)


def request(retries: int = 5, errorHandler: HTTPErrorHandler = HTTPErrorHandler(),
            exponentialBackoff: bool = False, delay: int = 1):
    """
    :param retries:
    :param errorHandler:
    :param exponentialBackoff:
    :param delay:
    :return Response:

    this is a decorator function that is ment to be used for functions sending requests to APIs

    requirements to use this decorator on a function:
        - function returns instance of requests.Response

    """
    def decorator(func: types.FunctionType):
        temp = delay  # wtf even is this ???

        def wrapper(*args, **kwargs):
            wait_time = temp
            tries = 0
            response = requests.Response()
            while tries < retries:
                response, status = errorHandler(lambda: func(*args, **kwargs))

                print(response.content)

                if status == 'ok':
                    return response

                if status == 'stop':
                    if response.status_code:
                        raise exceptions.TerminalStatusCode(response.status_code, func.__name__)
                    else:
                        raise exceptions.ExceptionInRequestFunction(func.__name__)

                tries += 1
                time.sleep(wait_time)
                if exponentialBackoff:
                    wait_time += 1

            raise exceptions.AllRetriesFailed(retries, response.status_code, func.__name__)

        return wrapper
    return decorator
