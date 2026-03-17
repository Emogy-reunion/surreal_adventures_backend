from core import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid



class Users(db.model):
    '''
    stores the user data
    '''
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

    def __init__(self, email, password):
        '''
        initializes the table with data
        '''
        self.email = email
        self.password_hash = hash_password(password)


        def hash_password(self, password):
            return bcrypt.generate_password_hash(password).decode('utf-8')
