from app import app, db
from flask import request, render_template, flash, redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from models import AssetItem, AssetType, PolicyItem, PolicyType, User
from forms import RegistrationForm, LoginForm, AssetForm, PolicyForm
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    else:
      login_user(user, form.remember_me.data)
      return redirect(f'/user/{user.id}')
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/user/<user_id>',methods=['GET', 'POST'])
@login_required
def user(user_id):
    user = current_user
    user = User.query.filter_by(email=user.email).first()
    policies = PolicyItem.query.filter_by(owner_id=user.id).all()
    if policies is None:
	    policies = []
    assets = AssetItem.query.filter_by(owner_id=user.id).all()
    if assets is None:
        assets = []
    asset_form = AssetForm()
    asset_form.asset_type.choices = [(asset_type.id, asset_type.description) for asset_type in AssetType.query.all()]
    if request.method == 'POST' and asset_form.validate():
        new_asset = AssetItem(
            asset_type = asset_form.asset_type.data,
            description=asset_form.description.data, 
            location=asset_form.location.data,
            owner_id=current_user.id
            )
        db.session.add(new_asset)
        db.session.commit()
    else:
        flash(asset_form.errors)
    asset_types = AssetType.query.all()
    return render_template('user.html', user=user, policies=policies, assets=assets, form=asset_form)

@app.route('/user/<user_id>/assets', methods=['GET', 'POST'])
@login_required
def assets(user_id):
    user = current_user
    user = User.query.filter_by(email=user.email).first()
    assets = AssetItem.query.filter_by(owner_id=user.id).all()
    if assets is None:
        assets = []
    asset_form = AssetForm()
    asset_form.asset_type.choices = [(asset_type.id, asset_type.description) for asset_type in AssetType.query.all()]
    if request.method == 'POST' and asset_form.validate():
        new_asset = AssetItem(
            asset_type = asset_form.asset_type.data,
            description=asset_form.description.data, 
            location=asset_form.location.data,
            owner_id=current_user.id
            )
        db.session.add(new_asset)
        db.session.commit()
    else:
        flash(asset_form.errors)
    assets = AssetItem.query.filter_by(owner_id=user.id).all()
    return render_template('assets.html', user=user, assets=assets, form=asset_form)

@app.route('/user/<user_id>/policies', methods=['GET', 'POST'])
@login_required
def policies(user_id):
    user = current_user
    user = User.query.filter_by(email=user.email).first()
    policy_items = PolicyItem.query.filter_by(owner_id=user.id).all()
    asset_items = AssetItem.query.filter_by(owner_id=user.id).all()
    if policy_items is None:
        policy_items = []
    policy_form = PolicyForm()
    policy_form.asset_item.choices = [(asset_item.id, asset_item.description) for asset_item in asset_items]
    policy_form.policy_type.choices = [(policy_type.id, policy_type.description) for policy_type in PolicyType.query.all()]
    if request.method == 'POST' and policy_form.validate():
        new_policy = PolicyItem(
            policy_type = policy_form.policy_type.data,
            asset_id = policy_form.asset_item.data,
            owner_id=current_user.id
            )
        db.session.add(new_policy)
        db.session.commit()
    else:
        flash(policy_form.errors)
    asset_items = AssetItem.query.filter_by(owner_id=user.id).all()
    policy_items = PolicyItem.query.filter_by(owner_id=user.id).all()
    return render_template('policies.html', user=user, assets=asset_items, policies=policy_items, form=policy_form)
    
@app.route('/')
def index():
    asset_types = AssetType.query.all()
    if not asset_types:
        asset_types=[]
    return render_template('landing_page.html',asset_types=asset_types)


