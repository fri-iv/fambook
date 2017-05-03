from apps import app
from flask import jsonify
from apps.users.decorators import login_required
from libs.tools import json_response, log, ws_response


@login_required
def note_create(user, data):
    try:
        note = user.note_create(data)
        note.changes_add(user, user.name + " created note '" + data['name'] + "'")

        if note:
            return ws_response(200, 'Note created successfully', note.id)

        return ws_response(400, "Can't create this note")
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return ws_response(400, "bitch, go away")


@login_required
def note_delete(user, data):
    try:

        if user.note_delete(data['id']):
            return ws_response(200, 'Note deleted successfully')

        return ws_response(400, 'Note could not be deleted')
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return ws_response(400, "bitch, go away")


@login_required
def note_get_list(user):
    try:
        notes = user.note_list_get()
        return ws_response(200, 'Notes list', notes)
    except:
        log()
        return ws_response(400, "Can't get notes")


@login_required
def item_add(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return ws_response(404, "Missing note")

    item = note.item_add(data['name'], data['description'])
    if item:
        return ws_response(200, 'Item added successfully', item.id)

    return ws_response(400, "Can't create new item")


@login_required
def item_delete(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return ws_response(404, "Missing note")

    if note.item_del(data['item_id']):
        return ws_response(200, 'Item deleted successfully')

    return ws_response(400, "Can't delete item")


@login_required
def item_mark(user, data):

    note = user.note_get(data['note_id'])

    if note.item_mark(data['item_id'], data['status']):
        checked = 'checked' if data['status'] else 'unchecked'

        return ws_response(200, 'Item ' + checked)

    return ws_response(400, "Can't change status")
