from peewee import *

from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Actor(BaseModel):
    id = AutoField()
    name = CharField()
    surname = CharField()

class Movie(BaseModel):
    id = AutoField()
    title = CharField()
    director = CharField()
    year = IntegerField()
    description = TextField()
    actors = ManyToManyField(Actor, backref='movies')

ActorMovie = Movie.actors.get_through_model()

db.connect()
db.create_tables([Actor, Movie, ActorMovie])
db.close()