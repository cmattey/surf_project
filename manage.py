import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from surf_app import app, db

"""
Contain our migration package object and a CLI Manager to
initialize(init), upgrade, migrate the database using the command line.

"""

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
