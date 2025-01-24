"""
Module for handling movie and actor management with FastApi
"""
from typing import List
from fastapi import FastAPI, HTTPException
#from fastapi import Depends
#import database
import schemas
import models
#from database import db_state_default
from schemas import ActorToMovie

app = FastAPI()

# Endpoint to get a list of all movies
@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    """
    Retrieve all movies from the database.
    Returns a list of movies.
    """
    return list(models.Movie.select())
    # movies = crud.get_movies()
    # return movies

#Endpoint to add a new movie to the database
@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    """
    Add a new movie to the database.
    Returns the added movie.
    """
    movie = models.Movie.create(**movie.dict())
    return movie

#Endpoint to get a single movie by its ID
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    """
    Retrieve a movie by its ID.
    Returns the movie if found, raises 404 otherwise.
    """
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# Endpoint to delete movie by its ID
@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    """
    Delete a movie by its ID.
    Returns the deleted movie if found, raises 404 otherwise.
    """
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie

# Endpoint to get a list of all actors
@app.get("/actors/", response_model=List[schemas.Actor])
def get_actors():
    """
    Retrieve all actors from the database.
    Returns a list of actors.
    """
    return list(models.Actor.select())

#Endpoint to get a single actor by their ID
@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int):
    """
    Retrieve an actor by its ID.
    Return the actor if found, raises 404 otherwise.
    """
    actor = models.Actor.get_or_none(models.Actor.id == actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

# Endpoint to add a new actor to the database
@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.ActorCreate):
    """
    Add a new actor to the database.
    Return the added actor.
    """
    actor = models.Actor.create(**actor.dict())
    return actor

# Endpoint to delete an actor by their ID
@app.delete("/actors/{actor_id}", response_model=schemas.Actor)
def delete_actor(actor_id: int):
    """
    Delete an actor by its ID.
    Return the deleted actor if found, raises 404 otherwise.
    """
    actor = models.Actor.get_or_none(models.Actor.id == actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    actor.delete_instance()
    return actor

# Endpoint to add an actor to a movie by their IDs
@app.post("/movies/{movie_id}/actors", response_model=schemas.Movie)
def add_actor_to_movie(movie_id: int, actor_data: ActorToMovie):
    """
    Add a new actor to a movie.
    Returns the updated movie.
    """
    actor_id = actor_data.actor_id  # Get actor_id from body

    movie = models.Movie.get_or_none(models.Movie.id == movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor = models.Actor.get_or_none(models.Actor.id == actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    if actor in movie.actors:
        raise HTTPException(status_code=409, detail="Actor already assigned to this movie")

    movie.actors.add(actor)
    return movie
