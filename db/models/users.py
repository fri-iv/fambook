from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base, db_session
import sys, traceback
import uuid
from hashlib import md5
from flask import session


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    token = Column(String)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "<Session(token='%s')>" % self.token


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    session = relationship("Session", backref='session')

    notes = relationship('Note2User', back_populates='user')
    changes = relationship('NoteChanges', back_populates='user')

    # users = relationship("Item", order_by='Item.id', backref="user")

    # def __init__(self, firstname, secondname, mail, passwd, role):
    #     self.name = firstname
    #     self.email = mail
    #     self.surname = secondname
    #     self.password = passwd
    #     self.moder = role

    def __repr__(self):
        return "<User(name='%s', fullname='%s', email='%s', password='%s')>" % (
                    self.name, self.surname, self.email, self.password)

    @classmethod
    def authorize(cls, email, passwd):
        data = User.filter(User.email == email, User.password == str(md5(passwd).hexdigest())).first()
        return data

    @classmethod
    def login(cls, email, password):
        try:
            user_model = cls.authorize(email, password)
            if user_model:
                if not user_model.session:
                    secret_key = str(uuid.uuid1())
                    session['token'] = secret_key

                    sess_obj = Session(secret_key)
                    db_session.add(sess_obj)

                    user_model.session = sess_obj
                    user_model.save()

                    db_session.commit()

                    return True
                else:
                    return False
            else:
                return False

        except Exception as Error:
            print 'login error: %s' % Error
            traceback.print_exc(file=sys.stdout)
            db_session.rollback()

            return False

    @classmethod
    def logout(cls, token):
        try:
            db_session.query(User).filter(Session.token == token).delete()
            db_session.commit()

            del session['token']

            return True
        except Exception as Error:
            print 'logout error: %s' % Error
            traceback.print_exc(file=sys.stdout)
            db_session.rollback()
            return False