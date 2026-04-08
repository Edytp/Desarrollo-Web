from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField("Nombre del producto", validators=[DataRequired(), Length(min=2, max=200)])

    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1, max=10000)])

    precio = FloatField("Precio", validators=[DataRequired(), NumberRange(min=0.01, max=100000)])

    submit = SubmitField("Guardar Producto")
