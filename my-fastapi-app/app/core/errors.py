#Base class for expected application-level errors
class AppError(Exception):
    
    status_code = 400
    code = "application_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

#Raised when a requested resource does not exist
class ResourceNotFoundError(AppError):
    
    status_code = 404
    code = "resource_not_found"