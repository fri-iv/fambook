from apps import app
from apps.users.decorators import login_required
from libs.tools import log, ws_response, get_user_by_id


@login_required
def note_create(user, data):
    import json
    try:
        print 'in note'
        print 'encoded:', data.encode('utf-8')
        # print 'encoded type:', type(data.encode('utf-8'))
        print 'data:', data
        print 'type:', type(data)
        print 'json: ', json.loads(data)
        data = json.loads(data)
        print 'json type:', type(data)
        # print 'itemId:', data['itemId']
        note = user.note_create(data)
        # note.changes_add(user, user.name + " created note '" + data['name'] + "'")
        print 'note:', note
        if note:
            print note
            # return ws_response(200, 'Note created successfully', dict(id=note.id))
            return dict(id=note.id)
        return dict(status=400, message="Can't create this note")
    except Exception as NoteCreatingError:
        log(NoteCreatingError)
        return dict(status=400, message="bitch, go away")


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
def note_get_list(user, data):
    import json
    try:
        notes = user.note_list_get()
        return json.dumps(notes)
    except Exception as e:
        print e
        # log()
        return dict(status=400, message="Can't get notes")


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
        return ws_response(200, 'Item ' + ('' if data['status'] else 'un' + 'checked'))

    return ws_response(400, "Can't change status")


@login_required
def note_share(user, data):
    from apps.notes.exceptions import NoteShareException

    user2 = get_user_by_id(data['user_id'])

    if not user2:
        return ws_response(404, 'User not found')

    try:
        if user.share(data['note_id'], user2):
            return ws_response(200, 'Note shared successfully')
    except NoteShareException:
        return ws_response(400, "Can't share note for this user")


@login_required
def note_archive(user, data):

    if user.note_archive(data['note_id'], data['status']):
        return ws_response(200, "Note" + ('' if data['status'] else 'un') + 'archived successfully')

    return ws_response(200, "Can't" + ('' if data['status'] else 'un') + 'archive note')
