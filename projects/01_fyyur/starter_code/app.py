#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
#This comment was used for testing purposes for git commits
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# TODO Done: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Shows', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id}, {self.name}>'

    # TODO Done: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Shows', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist ID: {self.id}, name: {self.name}>'
    # TODO Done: implement any missing fields, as a database migration using Flask-Migrate

# TODO Done: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'< Shows ID: {self.id}, artist_id: {self.artist_id}, venue_id: {self.venue_id}, start_time: {self.start_time}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO Done: replace with real venues data.
    #       num_shows should  be aggregated based on number of upcoming shows per venue.

    data = Venue.query.order_by('id').all()
    return render_template('pages/venues.html', areas=data)

#  Create Venue

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO:Done: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    
    venue = Venue(
    name = form.name.data,
    genres = form.genres.data,
    address = form.address.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_talent = form.seeking_talent.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data
    )

    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + form.name.data + ' was successfully listed!')

    except ValueError as error:
        print(error)
        flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        db.session.rollback()
        
    finally:
        db.session.close()
        return render_template('forms/new_venue.html', form=form)

    # on successful db insert, flash success
    # TODO:Done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

#  Search Venue

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO Done: replace with real venue data from the venues table, using venue_id

    data = Venue.query.get(venue_id)

    return render_template('pages/show_venue.html', venue=data)

#  Delete Venue

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        venue_name= venue.name;
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + venue_name + ' was successfully removed.')

    except ValueError as error:
        print(error)
        flash('An error occurred. Venue ' + venue_name + ' could not be removed.')
        db.session.rollback()

    finally:
        db.session.close()
        return render_template('forms/new_venue.html', form=form)
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Edit Venue

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO Done: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

#  Create Artist

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO:Done: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    
    artist = Artist(
    name = form.name.data,
    genres = form.genres.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_venue = form.seeking_venue.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data
    )

    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + form.name.data + ' was successfully listed!')

    except ValueError as error:
        print(error)
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        db.session.rollback()
        
    finally:
        db.session.close()
        return render_template('forms/new_artist.html', form=form)

    # on successful db insert, flash success
    # TODO:Done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

#  Search Artist

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO Done: replace with real venue data from the venues table, using venue_id
    data = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)

# Delete Artist

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        artist = Artist.query.get(artist_id)
        artist_name= artist.name;
        db.session.delete(artist)
        db.session.commit()
        flash('Artist ' + artist_name + ' was successfully removed.')

    except ValueError as error:
        print(error)
        flash('An error occurred. Artist ' + artist_name + ' could not be removed.')
        db.session.rollback()

    finally:
        db.session.close()
        return render_template('forms/new_artist.html', form=form)

#  Edit Artist

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    
    shows = Shows.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
            "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
            "start_time": format_datetime(str(show.start_time))
        })

    return render_template('pages/shows.html', shows=data)

#  Create Show

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: Done insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    
    shows = Shows(
    artist_id=form.artist_id.data,
    venue_id=form.venue_id.data,
    start_time=form.start_time.data
    )

    try:
        db.session.add(shows)
        db.session.commit()
        flash('Show was successfully booked!')

    except ValueError as error:
        print(error)
        flash('An error occurred. Shows could not be booked.')
        db.session.rollback()
        
    finally:
        db.session.close()
        return render_template('pages/home.html', form=form)

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
