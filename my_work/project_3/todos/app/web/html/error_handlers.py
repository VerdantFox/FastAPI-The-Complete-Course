from fastapi import Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.web import errors
from app.web.html.flash_messages import FlashCategory, FlashMessage

ERROR_TEMPLATE = "errors/general_error.html"


def register_error_handlers(app):
    @app.exception_handler(errors.UserNotValidatedError)
    async def not_logged_in_handler(
        request: Request, error: errors.UserNotValidatedError
    ):
        FlashMessage(
            msg="Login session expired. Please log in again.",
            category=FlashCategory.ERROR,
        )
        return RedirectResponse(request.url_for("html:login_get"))

    @app.exception_handler(errors.UserNotAuthenticatedError)
    async def not_logged_in_handler(
        request: Request, error: errors.UserNotAuthenticatedError
    ):
        FlashMessage(
            msg="Please log in to use that service.",
            category=FlashCategory.ERROR,
        )
        return RedirectResponse(request.url_for("html:login_get"))

    @app.exception_handler(errors.WebError)
    async def web_error_handler(request: Request, error: errors.WebError):
        return RedirectResponse(
            request.url_for("html:general_error").include_query_params(
                detail=error.detail, status_code=error.status_code
            )
        )
