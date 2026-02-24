import os
import logging
from flask import Flask, request, Response
import requests

LOG_LEVEL_STR = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TARGET_URL = os.environ.get("TARGET_URL", "https://www-r.housing-stat.ch").rstrip("/")


@app.route("/housing-stat/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    query_string = (
        f"?{request.query_string.decode('utf-8')}" if request.query_string else ""
    )
    url = f"{TARGET_URL}/{path}{query_string}"
    logger.info(f"Forwarding {request.method} request to: {url}")
    logger.debug(f"Headers: {dict(request.headers)}")

    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != "host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )
    logger.debug(f"Target responded with status: {resp.status_code}")

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [
        (k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers
    ]

    return Response(resp.content, resp.status_code, headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
