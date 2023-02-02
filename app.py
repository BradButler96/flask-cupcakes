"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Cupcakes12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/', methods=["GET", "POST"])
def homepage():

    cupcakes = Cupcake.query.all()
    form = AddCupcakeForm()

    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data 

        if form.image.data:
            db.session.add(Cupcake(flavor=flavor, size=size, rating=rating, image=image))
            db.session.commit()
        else:
            db.session.add(Cupcake(flavor=flavor, size=size, rating=rating))
            db.session.commit()

        return redirect("/")
    else:
        return render_template('index.html', cupcakes=cupcakes, form=form)


@app.route('/api/cupcakes')
def all_cupcakes():
    all_cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in all_cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cc_id>')
def get_cupcake(cc_id):
    cupcake = Cupcake.query.get_or_404(cc_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cc_id>', methods=['PATCH'])
def update_cupcake(cc_id):
    cupcake = Cupcake.query.get_or_404(cc_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cc_id>', methods=['DELETE'])
def delete_cupcake(cc_id):
    cupcake = Cupcake.query.get_or_404(cc_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')