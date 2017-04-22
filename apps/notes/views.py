from apps import app
from flask import jsonify
from apps.users.decorators import login_required
from libs.tools import json_response, log


@login_required
def note_create(user, data):
    try:
        note = user.note_create(data)
        note.changes_add(user, user.email + " created note '" + data['name'] + "'")

        if note:
            return json_response(200, 'Note created successfully', note.id)

        return json_response(200, "Can't create this note")
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return jsonify(400)


@login_required
def note_delete(user, data):
    try:

        if user.note_delete(data['id']):
            return json_response(200, 'Note deleted successfully')

        return json_response(200, 'Note could not be deleted')
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return jsonify(400)


@login_required
def note_get_list(user):
    try:
        notes = user.note_list_get()
        return json_response(200, 'Notes list', notes)
    except:
        log()
        return json_response(400, "Can't get notes")


@login_required
def item_add(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return json_response(400, "Missing note")

    item = note.item_add(data['name'], data['description'])
    if item:
        return json_response(200, 'Item added successfully', item.id)

    return json_response(400, "Can't create new item")


@login_required
def item_delete(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return json_response(400, "Missing note")

    if note.item_del(data['item_id']):
        return json_response(200, 'Item deleted successfully')

    return json_response(400, "Can't delete item")


@login_required
def item_mark(user, data):

    note = user.note_get(data['note_id'])

    if note.item_mark(data['item_id'], data['status']):
        checked = 'checked' if data['status'] else 'unchecked'

        return json_response(200, 'Item ' + checked)

    return json_response(400, "Can't change status")
