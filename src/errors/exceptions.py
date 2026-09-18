class APIError(Exception):
    def __init__(
        self,
        message,
        description,
        code="API_ERROR",
        status_code=400,
        level="error"
    ):
        super().__init__(message)
        self.message = message
        self.description = description
        self.code = code
        self.status_code = status_code
        self.level = level


class BadRequestError(APIError):
    def __init__(
        self,
        description,
        message="Error de validación en la solicitud."
    ):
        super().__init__(
            message=message,
            description=description,
            code="BAD_REQUEST",
            status_code=400
        )


class NotFoundError(APIError):
    def __init__(
        self,
        description,
        message="Recurso no encontrado."
    ):
        super().__init__(
            message=message,
            description=description,
            code="NOT_FOUND",
            status_code=404
        )


class ConflictError(APIError):
    def __init__(
        self,
        description,
        message="Conflicto de negocio."
    ):
        super().__init__(
            message=message,
            description=description,
            code="CONFLICT",
            status_code=409
        )