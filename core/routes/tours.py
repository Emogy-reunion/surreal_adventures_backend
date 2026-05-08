from flask import Blueprint, request, jsonify, current_app, send_from_directory
from core.utils.role import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from slugify import slugify
from core.forms import TourUploadForm
from core.models import User, Tour, TourImages, Country
from werkzeug.utils import secure_filename
import os
from core.extensions import db
from werkzeug.datastructures import MultiDict
from sqlalchemy.orm import selectinload
from sqlalchemy import desc

tour_bp = Blueprint('tour_bp', __name__)
saved_file_paths = []


@tour_bp.route('/tours', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_tour():
    '''
    allows admins and superadmins to upload tours
    '''
    try:

        data = request.form if request.form else {}
        files = request.files if request.files else {}
        current_user_id = uuid.UUID(get_jwt_identity())

        form = TourUploadForm(formData=MultiDict(data))

        if not form.validate():
            return jsonify({'errors': form.errors}), 400

        country_name = form.country.data.lower().strip()
        name = form.name.data.lower().strip()
        location = form.location.data.lower().strip()
        price = form.price.data
        duration = form.duration.data
        discount_start = form.discount_start.data
        discount_price = form.discount_price.data
        discount_end = form.discount_end.data
        description = form.description.data.strip()
        highlights = [highlight.strip() for highlight in form.highlights.data.splitlines() if highlight.strip()]
        includes = [include.strip() for include in form.includes.data.splitlines() if includes.strip()]
        excludes = [include.strip() for exclude in form.excludes.data.splitlines() if excludes.strip()]
        is_featured = form.is_featured.data
        is_active = form.is_active.data
        is_day_trip = form.is_day_trip.data
        category = form.category.data.lower().strip()
        start_date = form.start_date.data
        end_date = form.end_date.data
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

        tour = Tour(country_id=country_id, user_id=user_id, name=name,
                           location=location, price=price, description=description,
                           highlights=highlights, is_featured=is_featured, is_active=is_active,
                           is_day_trip=is_day_trip, includes=includes, excludes=excludes,
                           discount_price=discount_price, discount_start=discount_start, category=category,
                           discount=discount_end, start_date=start_date, end_date=end_date, duration=duration
                           )
        db.session.add(tour)
        db.session.flush()

        image_filenames = []
        for image in images:
            if image and image.filename:
                extension = image.filename.rsplit('.', 1)[-1].lower()
                filename = f"{uuid.uuid4()}.{extension}"
                filename = secure_filename(filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(file_path)
                image_filenames.append(filename)
                saved_file_paths.append(file_path)

        for index, filename in enumerate(image_filenames):
            img = TourImages(
                    filename=filename,
                    tour_id=tour.id,
                    is_cover=(index == 0)
            )
            db.session.add(img)

        db.session.commit()
        return jsonify({'success': 'Tour uploaded successfully!'}), 201

    except Exception as e:
        db.session.rollback()

        for file_path in saved_file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete file {file_path}")
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500
