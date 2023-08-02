import logging

logging_format = f"%(asctime)s LEVEL: %(levelname)s MSG: %(message)s"
logging.basicConfig(format=logging_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def function_logger(func):
    async def wrapper(*args, **kwargs):
        logger.debug(f"Entering the function: {func.__name__} with this params: {args}, {kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f"Finishing the function, return value: {result}")
        return result
    return wrapper

