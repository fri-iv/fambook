from apps import app
from flask import jsonify
from apps.users.decorators import login_required
from libs.tools import get_data, json_response, log


@app.route('/create-note', methods=['POST'])
@login_required
def note_create(user, data):
    try:
        note = user.note_create(data)

        if note:
            return json_response(200, 'Note created successfully', note.id)

        return json_response(200, "Can't create this note")
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return jsonify(400)


@app.route('/delete-note', methods=['POST'])
@login_required
def note_delete(user, data):
    try:

        if user.note_delete(data['id']):
            return json_response(200, 'Note deleted successfully')

        return json_response(200, 'Note could not be deleted')
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return jsonify(400)


@app.route('/add-item', methods=['POST'])
@login_required
def item_add(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return json_response(400, "Missing note")

    item = note.item_add(data['name'], data['description'])
    if item:
        return json_response(200, 'Item added successfully', item.id)

    return json_response(400, "Can't create new item")


@app.route('/delete-item', methods=['POST'])
@login_required
def item_delete(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return json_response(400, "Missing note")

    if note.item_del(data['item_id']):
        return json_response(200, 'Item deleted seccessfully')

    return json_response(400, "Can't delete item")


@app.route('/mark-item', methods=['POST'])
@login_required
def item_mark(user, data):

    note = user.note_get(data['note_id'])

    if note.item_mark(data['item_id'], data['status']):
        checked = 'checked' if data['status'] else 'unchecked'

        return json_response(200, 'Item ' + checked)

    return json_response(400, "Can't change status")
