
# from sqlalchemy import Table, create_engine
# from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalch import init_engine, db_connect, db_session


# warnings.filterwarnings("ignore")
uri = 'sqlite:///auth_db.sqlite'
# engine = init_engine(uri)
# conn = db_connect(engine)
db_auth = SQLAlchemy()

# class for the table Users
class Users(db_auth.Model):
    __tablename__ = "users"
    id = db_auth.Column(db_auth.Integer, primary_key=True)
    username = db_auth.Column('username', db_auth.String(15), unique=True, nullable=False)
    email = db_auth.Column('email', db_auth.String(50), unique=True)
    password = db_auth.Column('password', db_auth.String(80))
    def __repr__(self):
        return '<User %r>' % self.username
# Users_tbl = Table('users', Users.metadata)

# fuction to create table using Users class
def create_users_table(engine):
    Users.metadata.create_all(engine)

# create the table
# create_users_table()
# alternatively
# db_auth.create_all()
