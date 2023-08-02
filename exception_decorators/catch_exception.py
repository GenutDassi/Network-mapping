import fastapi
import pymysql
import scapy
import starlette
from fastapi import HTTPException
from scapy.error import Scapy_Exception
from starlette.authentication import AuthenticationError


def catch_exception(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        # db exception
        except pymysql.err.OperationalError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.OperationalError")
        except pymysql.err.ProgrammingError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.ProgrammingError")
        except pymysql.err.IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.IntegrityError")
        except pymysql.err.DataError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.DataError")
        except pymysql.err.InternalError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.InternalError")
        except pymysql.err.NotSupportedError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.NotSupportedError")
        except pymysql.err.InterfaceError as e:
            raise HTTPException(status_code=400, detail=f"pymysql.err.InterfaceError")
        #HTTP exception
        except starlette.exceptions.HTTPException as e:
            raise HTTPException(status_code=400, detail=f"starlette.exceptions.HTTPException")
        # except fastapi.RequestValidationError as e:
        #     raise HTTPException(status_code=400, detail=f"fastapi.RequestValidationError")
        # except fastapi.WebSocketException as e:
        #     raise HTTPException(status_code=400, detail=f"fastapi.WebSocketException")
        # except fastapi.SecurityBaseException as e:
        #     raise HTTPException(status_code=400, detail=f"fastapi.SecurityBaseException")
        # except fastapi.BackgroundTasks as e:
        #     raise HTTPException(status_code=400, detail=f"fastapi.BackgroundTasks")
        # except fastapi.HTTPException as e:
        #     raise HTTPException(status_code=400, detail=f"fastapi.HTTPException")
        # file exception
        except scapy.error.Scapy_Exception as e:
            # Catch any database connection-related errors here
            raise HTTPException(status_code=400, detail=f"file error :scapy.error.Scapy_Exception")
        # Authentication exception
        except AuthenticationError as e:
            # Catch any database connection-related errors here
            raise HTTPException(status_code=400, detail=f"Authentication Error")
            # global exception
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"ValueError")
        except TypeError as e:
            raise HTTPException(status_code=400, detail=f"TypeError")
        except IndexError as e:
            raise HTTPException(status_code=400, detail=f'IndexError')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Exception")

            return None

    return wrapper



