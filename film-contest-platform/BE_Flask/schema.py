from datetime import datetime
from src.models import db

# CNPM-115: RBAC Roles & User Roles
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # 'admin', 'organizer', 'judge', 'participant'

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)

# CNPM-120 & CNPM-122: Submission Lifecycle & Review Schema
class SubmissionReview(db.Model):
    __tablename__ = 'submission_reviews'
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(20), nullable=False) # 'accepted', 'rejected', 'pending'
    reason = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)
