import logging
import urllib.request

# Get an instance of a logger
logger = logging.getLogger(__name__)


def getMilitaryImageFile(image_url):
    try:
        image = urllib.request.urlretrieve(image_url)
    except Exception as e:
        image = None
        logger.error(
            '[Portal - getMilitaryImageFile] error desconhecido - {}'.format(e))
    finally:
        return image
