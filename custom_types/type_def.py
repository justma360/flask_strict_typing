from typing import Union
from flask import jsonify


class RaiseAPIException(Exception):
    status_code = 400

    def __init__(
        self, name: str, message: str, status_code: int = None, payload: dict = None
    ):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

        if payload is not None:
            self.response = {
                "code": self.status_code,
                "name": name,
                "message": message,
                "data": payload,
            }
        else:
            self.response = {
                "code": self.status_code,
                "name": name,
                "message": message,
            }

    def get_response(self):
        return jsonify(self.response)


def api_response(
    code: int, path: str, object: str, message: str = None, data: dict = None
):
    response = {"code": code, "path": path, "object": object}

    if message is not None:
        response["message"] = message

    if data is not None:
        response["data"] = data

    return response, code


def check_json(
    keys: list[str], json: dict, return_missing: bool = False
) -> Union[bool, list[str]]:
    if not isinstance(keys, list):
        keys = [keys]

    missing_keys = []
    json_keys = json.keys()

    for key in keys:
        if key not in json_keys:
            if return_missing == True:
                missing_keys.append(key)
            else:
                return False

    if return_missing == True and len(missing_keys) > 0:
        return missing_keys
    else:
        return True
