import functools
import logging

from fastapi import HTTPException, status

LOGGER = logging.getLogger(__name__)


def handle_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as value_error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(value_error)
            ) from value_error
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"{func.__name__.capitalize()} operation timed out",
            ) from None
        except Exception as error:
            LOGGER.error(f"Unexpected error in {func.__name__}: {error!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            ) from error

    return wrapper
