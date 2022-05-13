from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    EmailField,
    FloatField,
    PasswordField,
    RadioField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional


# Course form
class GolfcourseForm(FlaskForm):
    course_name = StringField(
        label="Namn",
        validators=[DataRequired(), Length(min=3, max=100, message="Felaktig längd")],
    )
    course_region = StringField(
        label="Region", validators=[DataRequired(), Length(max=50)]
    )
    course_country = StringField(
        label="Land", validators=[DataRequired(), Length(max=50)]
    )
    course_status = StringField(
        label="Status", validators=[DataRequired(), Length(max=50)]
    )
    from_date = DateField(label="Från datum", validators=[Optional()])
    to_date = DateField(label="Till datum", validators=[Optional()])
    undantag = StringField(label="Undantag/Kommentarer", validators=[Optional()])
    competition = StringField(label="Tävlingsveckor", validators=[Optional()])
    updated_by = StringField(
        label="Uppdaterat av", validators=[DataRequired(), Length(max=50)]
    )
    info_source = StringField(
        label="Källa", validators=[DataRequired(), Length(max=50)]
    )
    facebook_url = StringField(label="Facebook", validators=[Optional()])
    website_url = StringField(label="Hemsida", validators=[Optional()])
    booking_system = StringField(label="Bokning", validators=[Optional()])
    coordinates = StringField(label="Platskoordinater", validators=[Optional()])
    google_maps_url = StringField(label="Google Maps", validators=[Optional()])


# User form
class UserForm(FlaskForm):
    email = EmailField(
        label="E-post", validators=[DataRequired(), Length(min=3), Email()]
    )
    first_name = StringField(
        label="Förnamn", validators=[DataRequired(), Length(min=3, max=100)]
    )
    last_name = StringField(
        label="Efternamn", validators=[DataRequired(), Length(min=3, max=100)]
    )
    password1 = PasswordField(
        label="Lösenord", validators=[DataRequired(), Length(min=6, max=150)]
    )
    password2 = PasswordField(
        label="Lösenord", validators=[DataRequired(), Length(min=6, max=150)]
    )
