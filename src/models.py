from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_planets = db.Table(
    "favorite_planets",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("planet_id", db.ForeignKey("planet.id")),
)
favorite_characters = db.Table(
    "favorite_characters",
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("character_id", db.ForeignKey("character.id")),
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorite_planets = db.relationship("Planet", secondary=favorite_planets)
    favorite_characters = db.relationship("Character", secondary=favorite_characters)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "favorite_planets": list(map(lambda x: x.serialize(), self.favorite_planets)),
            "favorite_characters": list(map(lambda x: x.serialize(), self.favorite_characters))
            # do not serialize the password, it's a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.Text, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
            # do not serialize the password, it's a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
            # do not serialize the password, it's a security breach
        }



