class UnexpectedNoneError(RuntimeError):
    """
    Exception raised when an attribute of an object is unexpectedly None.

    This is raised when access of an optional class member that should never be None is required, and the value
    of said member is unexpectedly None
    """

    def __init__(self, obj: object, attr: str) -> None:
        """
        Initialize the custom exception raised when an attribute of an object is unexpectedly None.

        :param obj: The object containing the attribute that is None.
        :param attr: The name of the attribute that is unexpectedly None.
        """
        super().__init__(f"{obj.__class__.__name__}.{attr} is None unexpectedly")
