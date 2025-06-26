from ..extensions import db

# The blueprint for our 'product' table in the database.
class Product(db.Model):
    # Each of these attributes corresponds to a column in the table.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False) # Make description required
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')