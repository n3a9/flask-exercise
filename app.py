from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/users", methods=["GET", "POST"])
def retrieve_add_users():
    if request.method == "GET":
        team = request.args.get("team")
        data = db.get("users")
        if team is not None:
            data = [i for i in data if i["team"] == team]
        return create_response({"users": data})
    if request.method == "POST":
        param = request.get_json()
        if param is None:
            return create_response(
                status=422,
                message="No parameters were included when trying to create a user. Must include 'name', 'age', and 'team'.",
            )
        if param.get("name") is None:
            return create_response(
                status=422,
                message="Parameter 'name' was not included in request. Be sure to include 'name' when creating a user.",
            )
        if param.get("age") is None:
            return create_response(
                status=422,
                message="Parameter 'age' was not included in request. Be sure to include 'age' when creating a user.",
            )
        if param.get("team") is None:
            return create_response(
                status=422,
                message="Parameter 'team' was not included in request. Be sure to include 'team' when creating a user.",
            )
        new_user = {
            "name": param.get("name"),
            "age": param.get("age"),
            "team": param.get("team"),
        }
        return create_response(db.create("users", new_user), status=201)


@app.route("/users/<id>")
def get_user(id):
    if db.getById("users", int(id)) is None:
        return create_response(status=404, message="User not found in database.")
    else:
        data = {"user": db.getById("users", int(id))}
        return create_response(data)


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
