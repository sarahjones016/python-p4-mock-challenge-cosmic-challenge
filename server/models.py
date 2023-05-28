from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", backref='planet')

    serialize_rules = ('-missions.planet',)

    def __repr__(self):
        return f'<Planet {self.id}: {self.name}>'

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", backref='scientist')

    serialize_rules = ('-missions.scientist',)

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Name field is required")
        return name
    
    @validates('field_of_study')
    def validates_field(self, key, field_of_study):
        if not field_of_study:
            raise ValueError("Field of study is required")
        return field_of_study

    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}>'

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id')) 
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    serialize_rules = ('-scientist.missions', '-planet.missions',)

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Name field is required")
        return name
    
    @validates('scientist_id')
    def validates_scientist_id(self, key, scientist_id):
        if not scientist_id:
            raise ValueError("Scientist ID field is required")
        return scientist_id
    
    @validates('planet_id')
    def validates_planet_id(self, key, planet_id):
        if not planet_id:
            raise ValueError("Planet ID field is required")
        return planet_id
    

# add any models you may need. 