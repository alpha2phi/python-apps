import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

Base = declarative_base()


class Accounts(Base):
    __tablename__ = 'accounts'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    createdon = Column(DateTime, default=datetime.datetime.utcnow)
    lastlogin = Column(DateTime)
