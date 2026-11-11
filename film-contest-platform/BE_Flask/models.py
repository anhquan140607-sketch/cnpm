from datetime import datetime
from src.models import db

class AICheckResult(db.Model):
    __tablename__ = 'ai_check_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'duplicate' hoặc 'ai_generated'
    score = db.Column(db.Numeric(5, 4), nullable=False)
    matched_submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='SET NULL'), nullable=True)
    decision = db.Column(db.String(50), nullable=False, default='pending')  # 'pending', 'flagged', 'cleared'
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

class JudgeAssignment(db.Model):
    __tablename__ = 'judge_assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('contest_rounds.id', ondelete='CASCADE'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('judge_id', 'category_id', 'round_id', name='uq_judge_category_round'),
    )

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('judge_id', 'submission_id', name='uq_judge_submission_eval'),
    )

class EvaluationScore(db.Model):
    __tablename__ = 'evaluation_scores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id', ondelete='CASCADE'), nullable=False)
    criterion_id = db.Column(db.Integer, db.ForeignKey('scoring_criteria.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Numeric(4, 2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('evaluation_id', 'criterion_id', name='uq_eval_criterion'),
    )