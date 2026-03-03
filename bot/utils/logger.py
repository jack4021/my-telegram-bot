import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("bot").setLevel(logging.INFO)

logger = logging.getLogger(__name__)
