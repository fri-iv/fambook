import unittest
from apps.users.tests import AuthClientClass
from db.db import db_session
from apps.notes.models import Note, Note2User, NoteChanges, Item


class NotesClientClass(AuthClientClass):

    def __init__(self):
        AuthClientClass.__init__(self)
        self.register()
        self.login()

    def create_note(self, name='NEW_NOTE', status=False, items=None):
        data = {
            'name':     name,
            'status':   status,
            'items': list()
        }
        for item in items:
            data['items'].append(dict(
                name=item.name,
                description=item.description
            ))
        return self.json_request('/api/v1/create-note', data)

    def delete_note(self, note_id):
        data = {
            'id': note_id
        }
        return self.json_request('/api/v1/delete-note', data)

    def archive_note(self, note_id, status=True):
        data = {
            'id': note_id,
            'status': status
        }
        return self.json_request('/api/v1/archive-note', data)

    def add_item(self, note_id, name, description=''):
        data = {
            'note_id': note_id,
            'name': name,
            'description': description
        }
        return self.json_request('/api/v1/add-item', data)

    def delete_item(self, note_id, item_id):
        data = {
            'note_id': note_id,
            'item_id': item_id
        }
        return self.json_request('/api/v1/delete-item', data)

    def mark_item(self, note_id, item_id, status=False):
        data = {
            'note_id': note_id,
            'item_id': item_id,
            'status': status
        }
        return self.json_request('/api/v1/mark-item', data)

    def notes_list_get(self):
        return self.get_request('/api/v1/get-notes')

    def __del__(self):
        self.delete()


class TItem:
    def __init__(self, name='', description=''):
        self.name = name
        self.description = description


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

        items = list()
        items.append(TItem('eggs', 'immediately'))
        items.append(TItem('potato', '2 kilo'))

        response = self.note.create_note('NEW_NOTE', False, items)
        assert response['details'] == 'Note created successfully'
        assert type(response['body']) == int
        note_id = response['body']

        response = self.note.notes_list_get()
        print 'response',response
        assert response['body'][0]['name'] == 'NEW_NOTE'
        assert response['body'][0]['status'] == False
        assert response['body'][0]['items'][0]['name'] == 'eggs'

        response = self.note.add_item(note_id, 'bread', '2 items')
        assert response['details'] == 'Item added successfully'
        assert type(response['body']) == int
        item_id = response['body']

        response = self.note.mark_item(note_id, item_id, True)
        assert response['details'] == 'Item checked'

        response = self.note.mark_item(note_id, item_id, False)
        assert response['details'] == 'Item unchecked'

        response = self.note.delete_item(note_id, item_id)
        assert response['details'] == 'Item deleted successfully'

        response = self.note.delete_note(note_id)
        assert response['details'] == 'Note deleted successfully'
