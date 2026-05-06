from core.extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
import uuid
from slugify import slugify
from sqlalchemy import func


class BaseModel(db.Model):
    '''
    Base model that provides common timestamp fields for all models.
    This class is marked as abstract, meaning SQLAlchemy will not create a table
        for it directly. Instead, other models will inherit from it.
    '''
     # Mark this model as abstract so it is not created as a database table
    __abstract__  = True

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False
                           )
    modified_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now(),
                            nullable=False
                            )


class User(BaseModel):
    '''
    stores the user data
    has one to many relationship with destinations page
    one user can have many destinations

    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(255),
                     db.CheckConstraint("role IN ('member', 'admin', 'superadmin')",
                     name='user_role_check'),
                     server_default='member',
                     nullable=False
                     )
    destinations = db.relationship('Destination', back_populates='user', lazy='selectin')
    tours = db.relationship('Tour', back_populates='user', lazy='selectin')

    def __init__(self, email, password):
        '''
        initializes the table with data
        '''
        self.email = email
        self.password_hash = User.hash_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Country(BaseModel):
    '''
    stores the country names
    '''
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    destinations = db.relationship('Destination', back_populates='country', lazy='selectin')
    tours = db.relationship('Tour', back_populates='country', lazy='selectin')

class Destination(BaseModel):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False, index=True)
    country = db.relationship('Country', back_populates='destinations', lazy='selectin')

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    user = db.relationship('User', back_populates='destinations', lazy='selectin')

    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False, index=True)
    start_price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    highlights = db.Column(JSONB, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    category = db.Column(db.String(50), index=True)
    slug = db.Column(db.String(255), nullable=False, index=True)

    images = db.relationship('DestinationImages', back_populates='destination', lazy='selectin', cascade='all, delete-orphan')


    def destination_preview(self):
        '''
        returns the destination preview details
        '''

        cover = next((img for img in self.images if img.is_cover), None)

        if not cover and self.images:
            cover = self.images[0]

        return {
                'id': self.id,
                'name': self.name,
                'location': self.location,
                'start_price': str(self.start_price),
                'slug': self.slug,
                'is_featured': self.is_featured,
                "image": cover.url if cover else None        
                }



class DestinationImages(db.Model):
    '''
    stores images specific to a destination
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id', ondelete='CASCADE'), nullable=False)
    destination = db.relationship('Destination', back_populates='images')
    filename = db.Column(db.String(255), nullable=False, unique=True)
    is_cover = db.Column(db.Boolean, default=False, index=True)

class Tour(BaseModel):
    '''
    store planned tours data
    '''
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    user = db.relationship('User', back_populates='tours')

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', back_populates='tours', lazy='selectin')

    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False, index=True)
    duration = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, index=True)
    discount_start = db.Column(db.Date, nullable=True)
    discount_end = db.Column(db.Date, nullable=True)
    discount_price = db.Column(db.Numeric(10,2), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    description = db.Column(db.Text, nullable=False)
    includes = db.Column(JSONB, nullable=False)
    excludes = db.Column(JSONB, nullable=False)
    highlights = db.Column(JSONB, nullable=False)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=True, index=True)
    is_day_trip = db.Column(db.Boolean, default=False)
    images = db.relationship('TourImages', back_populates='tour', cascade='all, delete-orphan', lazy='selectin')

class TourImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id', ondelete='CASCADE'), nullable=False)
    tour = db.relationship('Tour', back_populates='images')
    filename = db.Column(db.String(255), nullable=False)


