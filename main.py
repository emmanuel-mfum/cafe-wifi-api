from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # Other way to serialize

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def make_bool(val: int) -> bool:
    """
        Takes in a numeric value and converts to boolean

        :param val: Expecting number
        :return: Boolean
        """
    return bool(int(val))


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()  # gets all the cafes in the database
    random_cafe = random.choice(cafes)  # select a random Cafe object
    # Turn our random_cafe SQLAlchemy Object into a JSON. This process is called serialization.
    # Alternate way (see Cafe class) : return jsonify(cafe=random_cafe.to_dict())
    return jsonify(cafe={
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
        "amenities": {
            "has_sockets": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi
        },
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "map_url": random_cafe.map_url,
        "name": random_cafe.name,
        "seats": random_cafe.seats
    })


@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()  # gets all the coffees
    all_cafes = {}
    for cafe in cafes:
        all_cafes[cafe.id] = cafe.to_dict()

    return jsonify(all_cafes=all_cafes)


@app.route("/search")
def search_cafe():
    query_location = request.args.get('loc')  # gets query location as query parameter
    cafe = Cafe.query.filter_by(location=query_location).first()  # try to get Cafe object
    if cafe:
        found_cafe = {"cafe": cafe.to_dict()}
        return jsonify(found_cafe)
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location"
        })


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_cafe():
    new_cafe = Cafe(can_take_calls=make_bool(request.form.get("calls")),
                    coffee_price=f"£{request.form.get('coffee_price')}",
                    has_sockets=make_bool(request.form.get("sockets")),
                    has_toilet=make_bool(request.form.get("toilet")),
                    has_wifi=make_bool(request.form.get("wifi")),
                    img_url=request.form.get("img_url"),
                    location=request.form.get("loc"),
                    map_url=request.form.get("map_url"),
                    name=request.form.get("name"),
                    seats=request.form.get("seats"))
    if new_cafe:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={
            "success": "Successfully added the new cafe"
        })
    else:
        return jsonify(response={
            "error": "Unable to add the new cafe"
        })


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe_to_update = Cafe.query.get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = f"£{new_price}"
        db.session.commit()
        # Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={
            "success": "Successfully updated the price."
        }), 200
    else:
        # 404 = Resource not found
        return jsonify(error={
            "Not Found": "Sorry a cafe with that id was not found in the database. "
        }), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    cafe_to_delete = Cafe.query.get(cafe_id)
    if cafe_to_delete and api_key == "TopSecretAPIKey":
        db.session.delete(cafe_to_delete)
        db.session.commit()
        # Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={
            "success": "Successfully deleted the record for this cafe."
        }), 200
    elif api_key != "TopSecretAPIKey":
        # 404 = Resource not found
        return jsonify(error=" Sorry that is not allowed. Make sure you have the correct api_key"), 403
    else:  # case the cafe does not exist
        return jsonify(error=" Sorry a cafe with that id was not found in the database"), 404


if __name__ == '__main__':
    app.run(debug=True)
