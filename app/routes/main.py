from flask import Blueprint, render_template
from ..models.product import Product

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/products')
def products():
    """
    This route fetches all products from the database and displays them
    on the public products page.
    """
    # Product.query.all() gets every product record from the database.
    all_products = Product.query.all()
    
    # We pass the list of products into our template under the variable name 'products'.
    return render_template('products.html', products=all_products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Route to display the details of a single product.
    """
    # Fetch the product by its ID from the database.
    # get_or_404 will automatically return a 404 Not Found page if the ID doesn't exist.
    product = Product.query.get_or_404(product_id)
    
    # Render a new template, passing the single product object to it.
    return render_template('product_detail.html', product=product)