from tornado.ioloop import IOLoop, PeriodicCallback
from utils import image_color
from datetime import datetime
import sqlite3


class Archiver(object):
    def __init__(self, locations, db="./archive.sql", callback_minutes=15, _ioloop=None):
        self.locations = locations
        self.callback_minutes = callback_minutes
        self.periodic_callback = None
        self.db = db
        self.ioloop = _ioloop or IOLoop.instance()
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db) as db:
                db.execute("CREATE TABLE archive(location VARCHAR(128), "
                           "R SMALLINT, G SMALLINT, B SMALLINT, time DATETIME);")
                db.commit()
        except sqlite3.OperationalError:
            pass

    def start(self):
        self.ioloop.add_callback(self.align_time)
        return self

    def align_time(self):
        now = datetime.now()
        num_minutes = self.callback_minutes - (now.minute % self.callback_minutes)
        num_seconds = num_minutes * 60 - now.second
        self.ioloop.call_later(num_seconds, self.log)

    def log(self):
        if self.periodic_callback is None:
            self.periodic_callback = PeriodicCallback(
                self.log,
                self.callback_minutes * 60 * 1000
            ).start()
        now = datetime.now()
        with sqlite3.connect(self.db) as db:
            for location, values in self.locations.items():
                color = image_color(**values)
                db.execute("insert into archive values (?, ?, ?, ?, ?)",
                           (location, *color, now))
            db.commit()

    def get_last_N(self, location, N):
        with sqlite3.connect(self.db) as db:
            data = db.execute('SELECT R, G, B, time '
                              'FROM archive '
                              'WHERE location = ? '
                              'ORDER BY time DESC '
                              'LIMIT ?', (location, N))
        return [{"time": t, "color": (R, G, B)} for R, G, B, t in data]
