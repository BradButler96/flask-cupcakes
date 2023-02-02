from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional

sizes = ['XS','S', 'M', 'L', 'XL']
ratings = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 
           6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

class AddCupcakeForm(FlaskForm):
    """Form for adding cupcakes"""

    flavor = StringField("Flavor", validators=[InputRequired(message="Flavor cannot be blank")])
    size = SelectField("Size", choices=[(size, size) for size in sizes], validators=[InputRequired(message="Size cannot be blank")])
    rating = SelectField("Rating", coerce=float, choices=[(rating, rating) for rating in ratings], validators=[InputRequired(message="Rating cannot be blank")])
    image = StringField("Image Link", validators=[Optional()])
