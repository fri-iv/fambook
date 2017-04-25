from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, db_session
from libs.tools import log
import uuid
from hashlib import md5
from flask import session
from apps.notes.models import Note2User


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship('User', back_populates='session')

    def __init__(self):
        self.token = str(uuid.uuid1())

    def __repr__(self):
        return "<Session(token='%s')>" % self.token


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    session = relationship("Session", back_populates='user', cascade='all,delete', lazy='dynamic')

    notes = relationship('Note2User', back_populates='user', cascade='all,delete', lazy='dynamic')
    changes = relationship('NoteChanges', back_populates='user', cascade='all,delete', lazy='dynamic')

    def __repr__(self):
        return "<User(email='%s', password='%s', session='%s')>" % (
                    self.email, self.password, self.session)

    def _delete_session(self):
        if self.session is not None:
            db_session.query(Session).filter(Session.user_id == self.id).delete()
            db_session.commit()

            if 'token' in session:
                del session['token']

    def _create_session(self):
        try:
            self._delete_session()

            sess = Session()
            sess.user = self
            session['token'] = sess.token
            db_session.add(sess)
            db_session.commit()

            # self.session = sess
            # db_session.commit()
        except Exception as newSessionError:
            db_session.rollback()
            log(newSessionError)
            session['token'] = None

    @classmethod
    def register(cls, email, passwd):
        try:
            user = db_session.query(User).filter(User.email == email).first()

            if user:
                return 0

            password = str(md5(passwd).hexdigest())
            user = User(email=email, password=password)
            user._create_session()

            db_session.add(user)
            db_session.commit()

            return user
        except Exception as RegisterUserError:
            log(ReferenceError)
            db_session.rollback()
            return 0

    @classmethod
    def authorize(cls, email, passwd):
        data = db_session.query(User).filter(User.email == email,
                                             User.password == str(md5(passwd).hexdigest())).first()
        return data

    @classmethod
    def login(cls, email, password):
        try:
            user_model = cls.authorize(email, password)
            if user_model:
                if not user_model.session or ('token' not in session) or (session['token'] is None):
                    user_model._create_session()
                    return user_model
                else:
                    return 1
            else:
                return 2
        except Exception as LoginUserError:
            log(LoginUserError)
            db_session.rollback()

            return 0

    def logout(self):
        try:
            self._delete_session()
            return True
        except Exception as LogoutError:
            log(LogoutError)
            db_session.rollback()
            return False

    def delete(self):
        try:
            self._delete_session()
            db_session.query(User).filter(User.id == self.id).delete()
            db_session.commit()
            return 1
        except Exception as UserDeletingError:
            log(UserDeletingError)
            db_session.rollback()
            return 0

    def note_get(self, note_id):
        for note2user in self.notes:
            if note2user.note.id == note_id:
                return note2user.note
        return None

    def note_list_get(self):
        return [record.note.serialize() for record in self.notes]

    def note_create(self, data):
        from apps.notes.models import Note, Note2User
        try:
            note = Note()
            note.name = data['name']
            note.status = data['status']
            db_session.add(note)
            db_session.commit()

            note2user = Note2User()
            note2user.note = note
            note2user.user_id = self.id
            db_session.add(note2user)
            db_session.commit()

            if 'items' in data:
                for item in data['items']:
                    note.item_add(item['name'], item['description'])

            db_session.commit()

            return note
        except Exception as NoteCreatingError:
            log(NoteCreatingError)
            db_session.rollback()
            return 0

    def note_delete(self, note_id):
        try:
            note = self.note_get(note_id)
            if not note:
                return 0

            db_session.delete(note)
            db_session.commit()

            return 1
        except Exception as NoteDeletingError:
            log(NoteDeletingError)
            return 0