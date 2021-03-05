from app import db
import models

db.create_all()

# Define initial asset types
house_asset = models.AssetType(id=1, description="House")
auto_asset = models.AssetType(id=2, description="Auto")
person_asset = models.AssetType(id=3, description="Person")
# Boat? Possessions? Pet?
db.session.add(house_asset)
db.session.add(auto_asset)
db.session.add(person_asset)

# Define initial policy types
fire_policy = models.PolicyType(id=1, description="House Fire", asset_type_id = 1, annual_price=5000)
flood_policy = models.PolicyType(id=2, description="House Flood", asset_type_id = 1, annual_price = 4000)
liability_policy = models.PolicyType(id=3, description="Auto Liability", asset_type_id = 2, annual_price = 3000)
collision_policy = models.PolicyType(id=4, description="Auto Collision", asset_type_id = 2, annual_price = 1500)
comprehensive_policy = models.PolicyType(id=5, description="Auto Comprehensive", asset_type_id = 2, annual_price = 1500)
umbrella_policy = models.PolicyType(id=6, description="Personal Umbrella", asset_type_id = 3, annual_price = 600)
db.session.add(fire_policy)
db.session.add(flood_policy)
db.session.add(liability_policy)
db.session.add(collision_policy)
db.session.add(comprehensive_policy)
db.session.add(umbrella_policy)

# Define intial user
jacob_user = models.User(id=1, firstname="Jacob", lastname="Ohlhausen", email="jaohlhausen@gmail.com")
jacob_user.set_password("Password1")
db.session.add(jacob_user)

# Commit changes
db.session.commit()