from core.extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
import uuid
from slugify import slugify



class User(db.Model):
    '''
    stores the user data
    has one to many relationship with destinations page
    one user can have many destinations

    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc)
                           )
    modified_at = db.Column(db.DateTime,
                            default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc)
                            )
    destinations = db.relationship('Destination', back_populates='user', lazy='selectin')
    tours = db.relationship('Tours', back_populates='user', lazy='selectin'

    def __init__(self, email, password):
        '''
        initializes the table with data
        '''
        self.email = email
        self.password_hash = hash_password(password)


        def hash_password(self, password):
            return bcrypt.generate_password_hash(password).decode('utf-8')



class Country(db.Model):
    '''
    stores the country names
    '''
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    destinations = db.relationship('Destination', back_populates='country', lazy='selectin')

    def __init__(self, name):
        '''
        initializes table with data
        '''
        self.name = name
        self.slug = self.generate_slug(name)

    @staticmethod
    def generate_slug(name):
        return slugify(name)

class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', back_populates='destinations', lazy='selectin')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('User', back_populates='destinations', lazy='selectin')

    name = db.Column(db.String(100), nullable=False)
    start_price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    highlights = db.Column(JSONB, nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))
    slug = db.Column(db.String(255), unique=True, nullable=False)

    images = db.relationship('DestinationImages', back_populates='destination', lazy='selectin', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc)
                           )
    modified_at = db.Column(db.DateTime,
                            default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc)
                            )

class DestinationImages(db.Model):
    '''
    stores images specific to a destination
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id', ondelete='CASCADE'), nullable=False)
    destination = db.relationship('Destination', back_populates='images')
    filename = db.Column(db.String(255), nullable=False, unique=True)

class Tour(db.Model):
    '''
    store planned tours data
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(d.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    user = db.relationship('User', back_populates='tours')

    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_start = db.Column(db.Date, nullable=True)
    discount_end = db.Column(db.Date, nullable=True)
    discount_price = db.Column(db.Numeric(10,2), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=False)
    includes = db.Column(JSONB, nullable=False)
    excludes = db.Column(JSONB, nullable=False)
    highlights = db.Column(JSONB, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_day_trip = db.Column(db.Boolean, default=False)
    images = db.relationship('TourImages', back_populates='tour', cascade='all, delete-orphan', lazy='selectin')

    created_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc)
                           )
    modified_at = db.Column(db.DateTime,
                            default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc)
                            )

class TourImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id', ondelete='CASCADE'), nullable=False)
    tour = db.relationship('Tour', back_populates='images')
    filename = db.Column(db.String(255), nullable=False)


