from core import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid



class Users(db.model):
    '''
    stores the user data
    '''
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime,
                           default: lambda: datetime.now(timezone.utc)
                           )
    modified_at = db.Column(db.DateTime,
                            default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc)
                            )
