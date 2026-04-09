class ApiCoreException(Exception):
    def __init__(self, error):
        super().__init__(error)


class TerminalStatusCode(ApiCoreException):
    def __init__(self, statusCode: int, functionName: str, traceback: str):
        super().__init__(f"function {functionName} got a terminal status code - HTTP {statusCode}\n{traceback}")


class ExceptionInRequestFunction(ApiCoreException):
    def __init__(self, functionName: str, traceback: str):
        super().__init__(f"function {functionName}: Exception occurred\n{traceback}")


class AllRetriesFailed(ApiCoreException):
    def __init__(self, retries: int, lastStatusCode: int, functionName: str, traceback: str):
        super().__init__(f"function {functionName}: all {retries} retries failed   last status code - HTTP {lastStatusCode}\n{traceback}")
