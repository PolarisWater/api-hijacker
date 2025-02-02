class ApiCoreError(Exception):
    def __init__(self, error):
        super().__init__(error)


class TerminalStatusCodeError(ApiCoreError):
    def __init__(self, statusCode: int, functionName: str):
        super().__init__(f"function {functionName} got a terminal status code - HTTP {statusCode}")


class ExceptionInRequestFunctionError(ApiCoreError):
    def __init__(self, functionName: str):
        super().__init__(f"function {functionName}: Exception occurred")


class AllRetriesFailedError(ApiCoreError):
    def __init__(self, retries: int, lastStatusCode: int, functionName: str):
        super().__init__(f"function {functionName}: all {retries} retries failed   last status code - HTTP {lastStatusCode}")
