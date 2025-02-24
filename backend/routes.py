from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=['GET'])
def get_pictures():
    """Returns all pictures."""
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Returns a specific picture by its id."""
    # Adjusting for 0-based index
    try:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return jsonify({"message": "Picture not found"}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=['POST'])
def create_picture():
    """Creates a new picture."""
    try:
        if not request.json or not 'id' in request.json:
            abort(400, description="Invalid input")
        new_picture = request.json
        if any(pic['id'] == new_picture['id'] for pic in data):
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
        data.append(new_picture)
        return jsonify(new_picture), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500


    ######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates an existing picture by its id."""
    try:
        if not request.json:
            abort(400, description="Invalid input")
        updated_picture = request.json
        picture = next((pic for pic in data if pic['id'] == id), None)
        if not picture:
            return jsonify({"message": "picture not found"}), 404
        for key in updated_picture:
            if key in picture:
                picture[key] = updated_picture[key]
        return jsonify(picture), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes a picture by its id."""
    try:
        picture = next((pic for pic in data if pic['id'] == id), None)
        if not picture:
            return jsonify({"message": "picture not found"}), 404
        data.remove(picture)
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500