import os
import logging
from typing import Tuple
from flask import Flask, jsonify, Response, request
from Models.supplier import Supplier
from exceptions.supplier_exception import WrongArgType, MissingContactInfo

######################################################################
# Get bindings from the environment
######################################################################
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "5000")


######################################################################
# Create Flask application
######################################################################
app = Flask(__name__)
app.logger.setLevel(logging.INFO)


######################################################################
# Storage for Suppliers
######################################################################
suppliers = {}


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    return (
        jsonify(
            name="Supplier"
        ),
        200,
    )


@app.route("/supplier", methods=["PUT"])
def create_supplier() -> Tuple[Response, int]:
    """ Creates a supplier and returns the ID """
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))
    if request_body is None:
        app.logger.info("bad request")
        return error_response("no request body", 400)
    if "name" not in request_body:
        return error_response("missing name", 400)
    new_id = len(suppliers) + 1
    new_name = request_body["name"]
    if "email" in request_body:
        email = request_body["email"]
    else:
        email = ""
    if "address" in request_body:
        address = request_body["address"]
    else:
        address = ""
    try:
        new_supplier = Supplier(
            name=new_name,
            id=new_id,
            email=email,
            address=address
        )
        suppliers[new_id] = new_supplier
        app.logger.info("created new supplier with id {}".format(new_id))
    except (MissingContactInfo, WrongArgType) as e:
        return error_response(str(e), 400)
    finally:
        return new_supplier.to_json(), 200

######################################################################
#   Convenience functions
######################################################################


def error_response(msg: str, error_code: int) -> Tuple[Response, int]:
    return jsonify(
        error=msg
    ), error_code


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.logger.info("*" * 70)
    app.logger.info("   Seleton Flask For Supplier   ".center(70, "*"))
    app.logger.info("*" * 70)
    import sys
    app.logger.info(sys.path)
    app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)
