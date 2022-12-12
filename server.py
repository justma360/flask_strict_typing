import logging
import json
from flask import Flask, request
from config.settings import logger
from custom_types.type_def import RaiseAPIException, api_response, check_json
from routes import status_route, camera_route
from config.settings import config

### Logging built in the Flask server (does not log to file)
# log = logging.getLogger("werkzeug")
# log.setLevel(logging.WARN)


mainApp = Flask(__name__)
mainApp.register_blueprint(status_route.status_route)
mainApp.register_blueprint(camera_route.camera_route)


### This handles all other exceptions in the server
@mainApp.errorhandler(Exception)
def http_error_handler(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "object": e.name,
            "message": f"{e.name} : {e.description}",
        }
    )
    response.content_type = "application/json"
    logger.error(response)
    return response


### this handles specific error such as typing errors
@mainApp.errorhandler(RaiseAPIException)
def handle_invalid_usage(error):
    response = error.get_response()
    logger.error(response)
    return response


### Logs to log all the requests made
@mainApp.before_request
def log_request_info():
    logger.info(request)


@mainApp.route("/example", methods=["GET", "POST"])
def status_online():
    if request.method == "GET":
        valid = check_json(["test", "testing"], request.json, return_missing=True)
        if valid == True:
            return api_response(
                code=200,
                path=str(request.url_rule),
                object="/example",
                message="Optional message here",
                data={"key": "value"},
            )
        else:
            raise RaiseAPIException(
                "Missing Field", f"You are missing {valid} field", status_code=400
            )

    raise RaiseAPIException(
        "Invalid Method", "The Method you are calling does not exist", status_code=404
    )


def start_server():
    mainApp.run(host=config["FLASK_IP"], port=config["FLASK_PORT"])
