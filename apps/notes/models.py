from sqlalchemy import Column, Integer, String, ForeignKey, \
    Boolean, DateTime
from db.db import Base, db_session
from sqlalchemy.orm import relationship


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    status = Column(Boolean, server_default='False')
    created_at = Column(DateTime, server_default='now()')

    items = relationship('Item', back_populates='note', lazy='dynamic', cascade='all,delete')
    changes = relationship('NoteChanges', back_populates='note', lazy='dynamic', cascade='all,delete')
    users = relationship('Note2User', back_populates='note', lazy='dynamic', cascade='all,delete')

    def item_add(self, name, description):

        item = Item()
        item.name = name
        item.description = description
        item.note_id = self.id
        db_session.add(item)

        self.items.append(item)
        db_session.commit()

        return item

    def item_del(self, item_id):

        self.items.filter(Item.id == item_id).delete()
        db_session.commit()

        return 1

    def item_mark(self, item_id, status):

        item = self.items.filter(Item.id == item_id).first()
        if not item_id:
            return 0

        item.status = status
        db_session.commit()

        return 1

    def changes_add(self, user, action=''):
        changes = NoteChanges()
        changes.user_id = user.id
        changes.note_id = self.id
        changes.action = action

        db_session.add_(changes)
        db_session.commit()

    def serialize(self):
        items = [dict(name=item.name, desciption=item.description) for item in self.items]
        users = [dict(uid=record.user.id, email=record.user.email) for record in self.users]
        changes = [dict(action=record.action, updated_at=record.updated_at) for record in self.changes]

        return dict(
            name=self.name,
            status=self.status,
            created_at=self.created_at,
            items=items,
            users=users,
            changes=changes
        )


class Note2User(Base):
    __tablename__ = 'notes_users_m2m'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='notes')
    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    note = relationship('Note', back_populates='users')


class NoteChanges(Base):
    __tablename__ = 'notes_changes'

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    updated_at = Column(DateTime, server_default='now()')

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='changes')
    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    note = relationship('Note', back_populates='changes')


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, server_default='False')

    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    note = relationship('Note', back_populates='items')
