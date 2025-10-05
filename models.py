from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone, "location": self.location}

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    quantity = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "farmer_id": self.farmer_id, "name": self.name, "type": self.type, "quantity": self.quantity}

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    buyer_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")

    def to_dict(self):
        return {"id": self.id, "crop_id": self.crop_id, "buyer_name": self.buyer_name, "quantity": self.quantity, "status": self.status}

class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(50), nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "crop_name": self.crop_name, "price_per_kg": self.price_per_kg}