from sqlalchemy import Column, Integer, String, ForeignKey, \
    Boolean, DateTime, func
from db.db import Base, db_session
from sqlalchemy.orm import relationship


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    status = Column(Boolean, server_default='False')
    created_at = Column(DateTime, server_default='now()')

    items = relationship('Item', back_populates='note')
    changes = relationship('NoteChanges', back_populates='note')
    users = relationship('Note2User', back_populates='note')


class Note2User(Base):
    __tablename__ = 'notes_users_m2m'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='notes')
    note_id = Column(Integer, ForeignKey('notes.id'), nullable=False)
    note = relationship('Note', back_populates='users')


class NoteChanges(Base):
    __tablename__ = 'notes_changes'

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    updated_at = Column(DateTime, server_default='now()')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='changes')
    note_id = Column(Integer, ForeignKey('notes.id'), nullable=False)
    note = relationship('Note', back_populates='changes')


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, server_default='False')

    note_id = Column(Integer, ForeignKey('notes.id'), nullable=False)
    note = relationship('Note', back_populates='items')
