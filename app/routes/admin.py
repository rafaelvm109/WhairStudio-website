# Import necessary tools from Flask and other packages
import os
import secrets
# Import the Pillow library for image processing
from PIL import Image
# Import necessary tools from Flask
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, session, request, abort
from flask_login import current_user, login_required
# Import our database and models/forms
from ..extensions import db
from ..forms import ProductForm
from ..models.product import Product


# Create the admin blueprint
admin = Blueprint('admin', __name__)

def save_picture(form_picture):
    """
    Handles the logic of saving an uploaded picture:
    1. Generates a random, secure filename.
    2. Resizes the image to a standard size.
    3. Saves the image to our filesystem.
    4. Returns the new filename.
    """
    # 1. Generate a random 8-byte hex string for the filename
    random_hex = secrets.token_hex(8)
    
    # 2. Get the file extension (e.g., '.jpg', '.png') from the uploaded file
    _, f_ext = os.path.splitext(form_picture.filename)
    
    # 3. Combine the random hex and the extension to create the new filename
    picture_fn = random_hex + f_ext
    
    # 4. Create the full path where the file will be saved
    # current_app.root_path gives us the absolute path to our project's root folder
    picture_path = os.path.join(current_app.root_path, 'static/product_pics', picture_fn)

    # 5. Resize the image before saving to save space and standardize dimensions
    output_size = (500, 500) # Set max height and width
    i = Image.open(form_picture)
    i.thumbnail(output_size) # This resizes the image while maintaining aspect ratio
    
    # 6. Save the processed image to the path
    i.save(picture_path)

    # 7. Return the new filename so we can store it in the database
    return picture_fn


@admin.before_request
@login_required
def before_request():
    """
    This function runs before every request to the admin blueprint.
    It protects all admin routes.
    """
    # First, @login_required ensures the user is logged in.
    # Then, we check if the logged-in user has the 'is_admin' flag.
    if not current_user.is_admin:
        # If they are not an admin, we abort the request and show a 403 Forbidden error.
        abort(403)
        

# This is the existing route for the main admin dashboard
@admin.route('/dashboard')
def dashboard():
    """
    The main admin dashboard.
    This route now fetches all products from the database to display them.
    """
    # Product.query.all() is a SQLAlchemy command to get every record
    # from the 'product' table.
    products = Product.query.all()
    
    # We pass the list of products to our template.
    return render_template('admin/dashboard.html', products=products)


@admin.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        # This is the new part: check if an image was uploaded with the form
        if form.image.data:
            # If so, call our helper function to save it and get the new filename
            picture_file = save_picture(form.image.data)
            # Create the Product with the custom image filename
            new_product = Product(
                name=form.name.data,
                price=form.price.data,
                description=form.description.data,
                image_file=picture_file  # Use the new filename
            )
        else:
            # If no image was uploaded, create the product without the image_file
            # The database will use the 'default.jpg' we set up in the model
            new_product = Product(
                name=form.name.data,
                price=form.price.data,
                description=form.description.data
            )

        db.session.add(new_product)
        db.session.commit()
        flash('Product has been added successfully!', 'success')

        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_product.html', title='Add Product', form=form)


@admin.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    """
    Route for updating an existing product.
    """
    # get_or_404 is a handy Flask-SQLAlchemy function that gets the product
    # by its ID, or returns a 404 Not Found error if it doesn't exist.
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    # This block runs when the admin submits the updated form
    if form.validate_on_submit():
        # First, check if a new image was uploaded
        if form.image.data:
            # If so, save the new picture and get its filename
            picture_file = save_picture(form.image.data)
            # Update the product's image_file attribute
            product.image_file = picture_file
        
        # Update the other attributes with the data from the form
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        
        # We only need to commit the changes, as the product is already in the session
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('admin.dashboard'))

    # This block runs when the admin first visits the page (GET request)
    # It pre-populates the form with the product's current data.
    elif request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.description.data = product.description

    return render_template('admin/update_product.html', title='Update Product', form=form, product=product)


@admin.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """
    Route to delete a product from the database.
    """
    # Fetch the product by its ID or return a 404 error if not found.
    product = Product.query.get_or_404(product_id)
    
    # --- Cleanup: Delete the associated image file ---
    # We should not delete the 'default.jpg' file.
    if product.image_file != 'default.jpg':
        try:
            # Construct the full path to the image file
            image_path = os.path.join(current_app.root_path, 'static/product_pics', product.image_file)
            # Delete the file from the filesystem
            os.remove(image_path)
        except FileNotFoundError:
            # If the file is not found, we can just ignore the error and proceed
            pass

    # Delete the product from the database session
    db.session.delete(product)
    # Commit the changes to permanently delete the record
    db.session.commit()
    
    flash('Product has been deleted.', 'success')
    return redirect(url_for('admin.dashboard'))