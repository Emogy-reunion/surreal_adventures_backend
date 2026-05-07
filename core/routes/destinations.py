from flask import Blueprint, request, jsonify, current_app
from core.utils.role import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from slugify import slugify
from core.forms import DestinationUploadForm
from core.models import User, Destination, DestinationImages, Country
from werkzeug.utils import secure_filename
import os
from core.extensions import db
from werkzeug.datastructures import MultiDict


dest_bp = Blueprint('dest_bp', __name__)
saved_file_paths = []


@dest_bp.route('/destinations', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_destination():
    '''
    allows admins and superadmins to upload destinations
    '''
    try:

        data = request.form if request.form else {}
        files = request.files if request.files else {}
        current_user_id = uuid.UUID(get_jwt_identity())

        form = DestinationUploadForm(formData=MultiDict(data))

        if not form.validate():
            return jsonify({'errors': form.errors}), 400

        country_name = form.country.data.lower().strip()
        name = form.name.data.lower().strip()
        location = form.location.data.lower().strip()
        start_price = form.start_price.data
        description = form.description.data.strip()
        highlights = [highlight.strip() for highlight in form.highlights.data.splitlines() if highlight.strip()]
        is_featured = form.is_featured.data
        category = form.category.data.lower().strip()
        slug = slugify(location)
        country_slug = slugify(country_name)
        images = request.files.getlist('images') 

        if not images or len(images) < 3:
            return jsonify({'error': 'Please upload at least 3 images to showcase the product clearly'}), 400

        if images and len(images) > 6:
            return jsonify({'error': 'You can upload a maximum of 6 images. Choose the most relevant ones.'}), 400

        user_id = db.session.query(User.id).filter_by(id=current_user_id).scalar()

        if not user_id:
            return jsonify({"error": 'User not found!'}), 404

        country_id = db.session.query(Country.id).filter_by(slug=country_slug).scalar()

        if not country_id:
            country = Country(name=country_name, slug=country_slug)
            db.session.add(country)
            db.session.flush()
            country_id = country.id

        destination = Destination(country_id=country_id, user_id=user_id, name=name,
                                  location=location, start_price=start_price, description=description,
                                  highlights=highlights, is_featured=is_featured, category=category, slug=slug)
        db.session.add(destination)
        db.session.flush()

        image_filenames = []
        for image in images:
            if image and image.filename:
                extension = image.filename.rsplit('.', 1)[-1].lower()
                filename = f"{uuid.uuid4()}.{extension}"
                filename = secure_filename(filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_filenames.append(filename)
                saved_file_paths.append(file_path)

        for index, filename in enumerate(image_filenames):
            img = DestinationImages(
                    filename=filename,
                    destination_id=destination.id,
                    is_cover=(index == 0)
            )
            db.session.add(img)

        db.session.commit()
        return jsonify({'success': 'Destination uploaded successfully!'}), 201

    except Exception as e:
        db.session.rollback()

        for file_path in saved_file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete file {file_path}")
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500


@dest_bp.route('/destinations', methods=['GET'])
def get_destinations():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))

        query = Destination.query.options(selectinload(Destination.images))

        paginated_results = (query
                    .order_by(desc(Destination.created_at))
                    .paginate(page=page, per_page=per_page, error_out=False)
                    )

        destinations = [destination.destination_preview() for destination in paginated_results.items] if paginated_results.items else []

        pagination = {
                'next': paginated_results.next_num if paginated_results.has_next else None,
                'prev': paginated_results.prev_num if paginated_results.has_prev else None,
                'page': paginated_results.page,
                'pages': paginated_results.pages,
                'total': paginated_results.total
                }

        return jsonify({
            'pagination': pagination,
            'destinations': destinations
            }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again'}), 500


@dest_bp.route('/destinations/<int: dest_id>', methods=['GET'])
def get_destination_details(dest_id):
    try:
        destination = Destination.query.options(selectinload(Destination.images)).filter_by(id=dest_id).first()

        destination_details = destination.destination_details() if destination else None

        return jsonify({'destination_details': destination_details}), 200
    else:
        return jsonify({'error': 'An unexpected error occurred. Please try again'}), 500
