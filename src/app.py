"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
data = (("John", 33, [7, 13, 22]),("Jane",35,[10, 14, 3]),("Jimmy",5,[1]))
for item in data:
    jackson_family.add_member({
        "first_name": item[0],
        "age": item[1],
        "lucky_numbers": item[2]
    })


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    try:
        if not member_id: return "", 400
        member = jackson_family.get_member(member_id)
        return jsonify(member), 200
    except Exception as err:
        return "", 500

@app.route('/member', methods=['POST'])
def handle_new_member():
    try:
        new_member = {**request.json}
        for item in ("first_name", "age", "lucky_numbers"):
            if not item in new_member:
                return "Lost %s property" % item, 400
        jackson_family.add_member(new_member)
        return 'EMPTY', 200
    except Exception as err:
        return "%s" % err, 500

@app.route("/member/<int:id>",methods=["DELETE"])
def delete_member (id):
    try:
        if not id: return "", 400
        jackson_family.delete_member(id)
        response = {
            "done": True
        }
        return jsonify(response), 200
    except Exception as err:
        return "", 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
