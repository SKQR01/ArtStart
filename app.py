from flask import Flask
from config import Conf
from flask_sqlalchemy import SQLAlchemy
import sqlite3

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask import Blueprint, render_template
from flask_login import LoginManager

### Инициализация приложения ###

app = Flask(__name__)
app.config.from_object(Conf)

### Создание БД ###

db = SQLAlchemy(app)

### Создание курсосра и соединения с БД ###

conn = sqlite3.connect(r"data/db.db")
cursor = conn.cursor()

login_manager = LoginManager(app)
login_manager.setup_app(app)

### Миграции ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


