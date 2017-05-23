from scraper import db
from datetime import datetime


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255))
    station_name = db.Column(db.String(255))
    district = db.Column(db.String(255))
    river_basin = db.Column(db.String(255))
    last_update = db.Column(db.DateTime)
    water_level = db.Column(db.Float(asdecimal=True))

    def __init__(self, station_name, district, river_basin, last_update, water_level, state):
        self.state = state
        self.station_name = station_name
        self.district = district
        self.river_basin = river_basin
        self.last_update = last_update
        self.water_level = water_level

    def __repr__(self):
        return '<Station %d>' % self.id
