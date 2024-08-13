from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String, nullable=False)

class TrimRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, db.ForeignKey('video.id'), nullable=False)
    trim_start = db.Column(db.Integer, nullable=False)
    trim_end = db.Column(db.Integer, nullable=False)

class ConcatRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_ids = db.Column(db.String, nullable=False)

class FinalVideo(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String, nullable=False)
