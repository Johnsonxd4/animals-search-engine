from flask_sqlalchemy import SQLAlchemy
import json
db = SQLAlchemy()
class Animal(db.Model): 
    __tablename__ = 'animals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specie = db.Column(db.String(100), unique=False, nullable=False)
    category = db.Column(db.String(100), unique=False, nullable=False)
    habitat = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f"<animal {self.name}>"
    
    def __init__(self, name,specie, category, habitat):
        self.name = name
        self.specie = specie
        self.category = category
        self.habitat = habitat

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'specie': self.specie,
            'category': self.category,
            'habitat': self.habitat
        })