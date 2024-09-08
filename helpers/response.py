from typing import Any
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class HttpResponse():

    @staticmethod
    def Ok(
        data: Any = None,
        message: str = "",
        status: str = "success",
        statusCode: int = 200):
        
        return Response(
            status=statusCode,
            data={
                "data": data,
                "message": message,
                "status": status,
                "statusCode": statusCode
            }
        )

    @staticmethod
    def Failed(
        message: str = "Internal Server Error",
        status: str = "failed",
        statusCode: int = 500,
        error: any = None):
        
        try:
            logger.error(error)
        except:
            pass
        
        return Response(
            status=statusCode,
            data={
                "message": message,
                "status": status,
                "statusCode": statusCode
            }
        )

    @staticmethod
    def BadRequest(
        message: str = "Bad Request",
        status: str = "failed",
        statusCode: int = 400):
        
        return Response(
            status=statusCode,
            data={
                "message": message,
                "status": status,
                "statusCode": statusCode
            }
        )
    
    @staticmethod
    def NotFound(
        message: str = "Not Found",
        status: str = "failed",
        statusCode: int = 404):
        
        return Response(
            status=statusCode,
            data={
                "message": message,
                "status": status,
                "statusCode": statusCode
            }
        )
