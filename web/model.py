# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Daycare(db.Model):
    __tablename__ = 'daycare'

    ch_id = db.Column(db.Integer, primary_key=True)
    locate = db.Column(db.Text, nullable=False)
    ch_name = db.Column(db.Text, nullable=False)
    ceo_name = db.Column(db.Text, nullable=False)
    tell_num1 = db.Column(db.Text, nullable=False)
    tell_num2 = db.Column(db.Text, nullable=False)
    tell_num3 = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)



class ReportList(db.Model):
    __tablename__ = 'report_list'

    police_num = db.Column(db.Integer, primary_key=True)
    video_fk = db.Column(db.Integer, nullable=False)
    locate = db.Column(db.Text, nullable=False)
    ch_fk = db.Column(db.Integer, nullable=False)
    report_time = db.Column(db.Integer, nullable=False)
    police_name = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)



class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_pw = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.Text, nullable=False)
    office_num = db.Column(db.Integer, nullable=False)
    locate = db.Column(db.Text, nullable=False)
    dept = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    ph_num1 = db.Column(db.Text, nullable=False)
    ph_num2 = db.Column(db.Text, nullable=False)
    ph_num3 = db.Column(db.Text, nullable=False)



class Video(db.Model):
    __tablename__ = 'video'

    video_id = db.Column(db.Integer, primary_key=True)
    locate = db.Column(db.Text, nullable=False)
    video_time = db.Column(db.Integer, nullable=False)
    ch_fk = db.Column(db.Integer, nullable=False)
    video_name = db.Column(db.Text, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    user_fk = db.Column(db.Integer, nullable=False)
