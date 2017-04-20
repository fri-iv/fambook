import unittest
from apps.users.tests import AuthClientClass
from db.db import db_session
from apps.notes.models import Note, Note2User, NoteChanges, Item


class NotesClientClass(AuthClientClass):

    def __init__(self):
        AuthClientClass.__init__(self)
        self.register()
        self.login()

    def create_note(self, name='NEW_NOTE', status=False):
        data = {
            'name':     name,
            'status':   status,
            'items': [
                {
                    'name': 'eggs',
                    'description': 'immediately'
                },
                {
                    'name': 'potato',
                    'description': '2 kilo'
                }
            ]
        }
        return self.json_request('/create-note', data)

    def delete_note(self, note_id):
        data = {
            'id': note_id
        }
        return self.json_request('/delete-note', data)

    def archive_note(self, note_id, status=True):
        data = {
            'id': note_id,
            'status': status
        }
        return self.json_request('/archive-note', data)

    def add_item(self, note_id, name, description=''):
        data = {
            'note_id': note_id,
            'name': name,
            'description': description
        }
        return self.json_request('/add-item', data)

    def delete_item(self, note_id, item_id):
        data = {
            'note_id': note_id,
            'item_id': item_id
        }
        return self.json_request('/delete-item', data)

    def mark_item(self, note_id, item_id, status=False):
        data = {
            'note_id': note_id,
            'item_id': item_id,
            'status': status
        }
        return self.json_request('/mark-item', data)

    def __del__(self):
        self.delete()


class NotesTestCase(unittest.TestCase):

    def setUp(self):
        self.note = NotesClientClass()
        self.initial_note_counter = db_session.query(Note).count()
        self.initial_note2user_counter = db_session.query(Note2User).count()
        self.initial_items_counter = db_session.query(Item).count()

    def tearDown(self):
        assert self.initial_items_counter == db_session.query(Item).count()
        assert self.initial_note2user_counter == db_session.query(Note2User).count()
        assert self.initial_note_counter == db_session.query(Note).count()

    def test_note(self):
        response = self.note.create_note()
        assert response['details'] == 'Note created successfully'
        assert type(response['body']) == int
        note_id = response['body']

        response = self.note.add_item(note_id, 'bread', '2 items')
        assert response['details'] == 'Item added successfully'
        assert type(response['body']) == int
        item_id = response['body']

        response = self.note.mark_item(note_id, item_id, True)
        assert response['details'] == 'Item checked'

        response = self.note.mark_item(note_id, item_id, False)
        assert response['details'] == 'Item unchecked'

        response = self.note.delete_item(note_id, item_id)
        assert response['details'] == 'Item deleted seccessfully'

        response = self.note.delete_note(note_id)
        assert response['details'] == 'Note deleted successfully'
