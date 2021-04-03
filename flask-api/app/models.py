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

    UserId = Column(Integer, primary_key=True)
    UserName = Column(String)
    Password = Column(String)
    Email = Column(String)
    CreatedOn = Column(DateTime)
    LastLogin = Column(DateTime)
