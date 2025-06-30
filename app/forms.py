from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from .models.user import User
from wtforms import BooleanField
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Senha', 
                             validators=[DataRequired(), Length(min=6)])
    
    confirm_password = PasswordField('Confirmar Senha', 
                                     validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Registre-se')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


class ProductForm(FlaskForm):
    """
    Form for an admin to add or edit a product.
    This class defines the structure and validation rules for our product form.
    """
    # StringField for the product's name.
    # DataRequired means this field cannot be empty.
    # Length sets a min and max character count.
    name = StringField('Nome do Produto', 
                       validators=[DataRequired(), Length(min=2, max=100)])
    
    # DecimalField is ideal for prices to avoid floating-point math errors.
    # We set places=2 for cents and rounding=None to be explicit.
    # NumberRange ensures the price is a positive number.
    price = DecimalField('Preço ($)', 
                         places=2, 
                         rounding=None,
                         validators=[DataRequired(), NumberRange(min=0)])
    
    # TextAreaField provides a larger, multi-line text box for the description.
    description = TextAreaField('Descrição', 
                                validators=[DataRequired()])
    
    # FileField will render as an <input type="file"> in HTML.
    # The 'FileAllowed' validator is crucial for security. It ensures
    # that only files with the specified extensions can be submitted.
    image = FileField('Adicionar Imagem', 
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    # The submit button for the form.
    submit = SubmitField('Salvar Produto')