from flask import Flask, request, jsonify, make_response
from http import HTTPStatus
import uuid

app = Flask(__name__)

DUMMY_RESOURCES = {}


def resource_url(integration_id):
    return f"http://dummy-eeba:9000/dummy-eeba/integrations/{integration_id}"


def create_resource_with_id(integration_id, ebau_id=None):
    resource = {
        "id": integration_id,
        "status": "completed",
        "relation": {
            "type": ".eBau",
            "eBauId": ebau_id or 123,
            "webUrl": resource_url(integration_id),
            "declarationOfWasteDisposalRequired": True,
        },
        "hint": None,
    }
    DUMMY_RESOURCES[integration_id] = resource
    return resource


@app.route("/dummy-eeba/integrations/", methods=["POST"])
def create_integration():
    data = request.json or {}
    integration_id = str(uuid.uuid4())
    ebau_id = data.get("relation", {}).get("eBauId")
    resource = create_resource_with_id(integration_id, ebau_id)
    DUMMY_RESOURCES[integration_id] = resource
    resp = make_response(jsonify(resource), HTTPStatus.CREATED)
    resp.headers["Location"] = f"/dummy-eeba/integrations/{integration_id}"
    return resp


@app.route("/dummy-eeba/integrations/<integration_id>", methods=["GET"])
def retrieve_integration(integration_id):
    resource = DUMMY_RESOURCES.get(integration_id)
    if not resource:
        return jsonify(
            {
                "errors": [
                    {
                        "field": "NoSuchElementException",
                        "errorCode": "NoSuchElementException",
                        "message": "No value present",
                    }
                ]
            }
        ), HTTPStatus.NOT_FOUND
    # Simulate state change:
    if resource["status"] == "init":
        resource["status"] = "inProgress"
    elif resource["status"] == "inProgress":
        resource["status"] = "completed"
        resource["hint"] = "Integration completed!"
    return jsonify(resource), HTTPStatus.OK


@app.route("/dummy-eeba/integrations/<integration_id>", methods=["PATCH"])
def partial_update_integration(integration_id):
    resource = DUMMY_RESOURCES.get(integration_id)
    if not resource:
        return jsonify(
            {
                "errors": [
                    {
                        "field": "NoSuchElementException",
                        "errorCode": "NoSuchElementException",
                        "message": "No value present",
                    }
                ]
            }
        ), HTTPStatus.NOT_FOUND
    data = request.json or {}
    print(request.json)
    # Update timeout if present
    if "timeout" in data:
        resource["timeout"] = data["timeout"]
    # Update eBauId if present in relation
    if "relation" in data and "eBauId" in data["relation"]:
        resource["relation"]["eBauId"] = data["relation"]["eBauId"]
    return "", HTTPStatus.NO_CONTENT


@app.route("/dummy-eeba/integrations/<integration_id>/rerun", methods=["POST"])
def rerun_integration(integration_id):
    resource = DUMMY_RESOURCES.get(integration_id)
    if not resource:
        create_resource_with_id(integration_id)
    else:
        resource["status"] = "completed"
        resource["hint"] = "Integration completed!"
    return "", HTTPStatus.NO_CONTENT


@app.route("/dummy-eeba/integrations/<integration_id>/retry", methods=["POST"])
def retry_integration(integration_id):
    resource = DUMMY_RESOURCES.get(integration_id)
    if not resource:
        create_resource_with_id(integration_id)
    else:
        resource["status"] = "completed"
        resource["hint"] = "Integration completed!"
    return "", HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    app.run(debug=True)
