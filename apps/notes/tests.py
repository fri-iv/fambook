import unittest
from apps.users.tests import AuthClientClass
from db import db_session
from apps.notes.models import Note, Note2User, NoteChanges, Item


class NotesClientClass(AuthClientClass):

    def __init__(self):
        from apps.facebook.facebook_api import FacebookTestUser

        fb_user = FacebookTestUser('Yanukovych Viktor')
        AuthClientClass.__init__(self, fb_user.access_token)
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
        return self.emit_request('/api/v1/create-note', data)

    def delete_note(self, note_id):
        data = {
            'id': note_id
        }
        return self.emit_request('/api/v1/delete-note', data)

    def archive_note(self, note_id, status=True):
        data = {
            'note_id': note_id,
            'status': status
        }
        return self.emit_request('/api/v1/archive-note', data)

    def share_note(self, note_id, user_id):
        data = {
            'note_id': note_id,
            'user_id': user_id
        }
        return self.emit_request('/api/v1/archive-note', data)

    def add_item(self, note_id, name, description=''):
        data = {
            'note_id': note_id,
            'name': name,
            'description': description
        }
        return self.emit_request('/api/v1/add-item', data)

    def delete_item(self, note_id, item_id):
        data = {
            'note_id': note_id,
            'item_id': item_id
        }
        return self.emit_request('/api/v1/delete-item', data)

    def mark_item(self, note_id, item_id, status=False):
        data = {
            'note_id': note_id,
            'item_id': item_id,
            'status': status
        }
        return self.emit_request('/api/v1/mark-item', data)

    def notes_list_get(self):
        return self.emit_request('/api/v1/get-notes')

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
        self.assertIn('name', response)
        note_id = response['id']

        response = self.note.notes_list_get()
        assert len(response) > 0
        assert not response[0]['status']
        assert response[0]['items'][0]['name'] == 'eggs'

        response = self.note.add_item(note_id, 'bread', '2 items')
        self.assertIn('name', response)

        item_id = None
        for item in response['items']:
            if item['name'] == 'bread' and item['name'] == 'bread':
                item_id = item['id']
                break

        response = self.note.mark_item(note_id, item_id, True)
        self.assertIn('successfully', response)

        response = self.note.mark_item(note_id, item_id, False)
        self.assertIn('successfully', response)

        response = self.note.delete_item(note_id, item_id)
        self.assertIn('successfully', response)

        response = self.note.archive_note(note_id, True)
        self.assertIn('successfully', response)

        response = self.note.archive_note(note_id, False)
        self.assertIn('successfully', response)

        response = self.note.delete_note(note_id)
        self.assertIn('successfully', response)