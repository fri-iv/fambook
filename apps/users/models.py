from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, db_session
# from libs.tools import log
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
    sid = Column(String)  # for websockets

    def __init__(self):
        self.token = str(uuid.uuid1())

    def __repr__(self):
        return "<Session(token='%s')>" % self.token


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fb_uid = Column(String)
    session = relationship("Session", back_populates='user', cascade='all,delete', lazy='dynamic')
    name = Column(String)

    notes = relationship('Note2User', back_populates='user', cascade='all,delete', lazy='dynamic')
    changes = relationship('NoteChanges', back_populates='user', cascade='all,delete', lazy='dynamic')

    def __repr__(self):
        return "<User(fb_uid='%s', name='%s', session='%s')>" % (
                    self.fb_uid, self.name, self.session)

    @property
    def avatar_url(self):
        return 'https://graph.facebook.com/v2.9/' + self.fb_uid + '/picture?width=315&height=315'

    def _delete_session(self):
        if self.session is not None:
            db_session.query(Session).filter(Session.user_id == self.id).delete()
            db_session.commit()

    def _create_session(self, ws_sid, fb_token):
        try:
            self._delete_session()

            sess = Session()
            sess.user = self
            sess.token = fb_token
            sess.sid = ws_sid
            db_session.add(sess)
            db_session.commit()

        except Exception as newSessionError:
            db_session.rollback()
            # log(newSessionError)
            session['token'] = None

    @classmethod
    def _register(cls, uid, last_name):
        user = User(fb_uid=uid, name=last_name)
        db_session.add(user)

        db_session.commit()
        return user


    @classmethod
    def login(cls, ws_sid, fb_token):
        from apps.facebook.facebook_api import FacebookUser, AuthError

        try:
            resp = FacebookUser(fb_token)
        except AuthError:
            return None

        user = db_session.query(User).filter(User.fb_uid == resp.result['id']).first()
        if not user:
            user = cls._register(resp.result['id'], resp.result['name'])

        user._create_session(ws_sid, fb_token)
        return user

    def logout(self):
        try:
            self._delete_session()
            return True
        except Exception as LogoutError:
            # log(LogoutError)
            db_session.rollback()
            return False

    def delete(self):
        try:
            self._delete_session()
            db_session.query(User).filter(User.id == self.id).delete()
            db_session.commit()
            return 1
        except Exception as UserDeletingError:
            # log(UserDeletingError)
            db_session.rollback()
            return 0

    def note_get(self, note_id):
        for note2user in self.notes:
            if note2user.note.id == note_id:
                return note2user.note
        return None

    def note_list_get(self):
        return [record.note.serialize() for record in self.notes] or []

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
            # log(NoteCreatingError)
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
            # log(NoteDeletingError)
            return 0

    def note_share(self, note_id, user):
        from apps.notes.exceptions import NoteShareException
        note = self.note_get(note_id)

        note2user = db_session.query(Note2User).filter(Note2User.user == user,
                                                       Note2User.note == note).first()
        if note2user:
            raise NoteShareException('already shared')

        note2user = Note2User(note=note,
                              user=user)
        db_session.add(note2user)
        db_session.commit()

        return True

    def note_archive(self, note_id, status):
        from apps.notes.exceptions import NoteExistingException
        note = self.note_get(note_id)

        if not note:
            raise NoteExistingException('doesnt exists')

        note.archive(status)
        return True
