from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    lastname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    policies = db.relationship('PolicyItem', backref='customer', lazy='dynamic')
    assets = db.relationship('AssetItem', backref='owner', lazy='dynamic')
  
    def __repr__(self):
        return '<User {}>'.format(self.email)
  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

class PolicyItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_item.id'))
    policy_type = db.Column(db.String(140), index=True)
    description = db.Column(db.String(140), index=True)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Policy {}>'.format(self.description)

class AssetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_type = db.Column(db.String(140), index=True)
    description = db.Column(db.String(140), index=True)
    location = db.Column(db.String(140), index=True)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    policies = db.relationship('PolicyItem', backref='asset', lazy='dynamic')

    def __repr__(self):
        return '<Asset {}>'.format(self.description)

class PolicyType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), index=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    annual_price = db.Column(db.Float)

    def __repr__(self):
        return '<Policy Type {}>'.format(self.description)

class AssetType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), index=True)
    policy_types = db.relationship('PolicyType', backref='asset_type', lazy='dynamic')

    def __repr__(self):
        return '<Asset Type {}>'.format(self.description)
