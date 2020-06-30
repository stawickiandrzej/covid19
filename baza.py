import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

user = User("admin","password")
session.add(user)

user = User("Andrzej","kLeJ27")
session.add(user)

user = User("user99","MorzE72")
session.add(user)

user = User("user72","małeNIC")
session.add(user)

user = User("user27","wielkieNIC")
session.add(user)

user = User("Janusz","e3grh8igmf8gm")
session.add(user)

user = User("Piotr","nothanks")
session.add(user)

session.commit()

session.commit()

