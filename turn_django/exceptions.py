from rest_framework import status
from rest_framework.views import set_rollback
from rest_framework.response import Response
from rest_framework.views import exception_handler


class Http_error( Exception ):
    """
    exception generic

    Arguments
    ---------
    status_code: int
    context: string, dict or list
    """
    def __init__(
            self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            context=None ):
        # if the context is a string return the format detail
        if context is None:
            context = 'Unhandled error.'
        if isinstance( context, ( str, ) ):
            context = { 'detail': context }
        self.status_code = status_code
        self.context = context


class Http_internal_server_error( Http_error ):
    """
    alias for the class py:class:`~Http_error`
    """
    pass


class Http_not_found( Http_error ):
    """
    excepcion for 404

    Arguments
    ---------
    context: string, dict or list
    """
    def __init__( self, context=None ):
        if context is None:
            context = 'Not found'
        super().__init__(
            context=context, status_code=status.HTTP_404_NOT_FOUND )


class Http_bad_request( Http_error ):
    """
    Excepticion for 400

    Arguments
    ---------
    context: string, dict or list
    """
    def __init__( self, context=None ):
        if context is None:
            context = 'unhandled parameters'
        super().__init__(
            context=context, status_code=status.HTTP_400_BAD_REQUEST )


def generic_exception_handler( exc, context ):
    """
    manage all uncatch exceptions

    Parameters
    ----------
    exc: Exception
    contex: object

    Notes
    -----
    the generic exceptions can handle are:
        * :class:`~Http_error`
        * :class:`~Http_not_found`
        * :class:`~Http_internal_server_error`
        * :class:`~Http_bad_request`

    also support the default exceptions of django
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler( exc, context )

    if isinstance( exc, Http_error ):
        response = Response( exc.context, status=exc.status_code )
        set_rollback()

    return response
