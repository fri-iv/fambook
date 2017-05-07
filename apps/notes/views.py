from apps import app
from apps.users.decorators import login_required
from libs.tools import ws_response, ws_error, ws_callback, get_user_by_id


@login_required
def note_create(user, data):

    note = user.note_create(data)

    if note:
        return ws_callback(note.serialize())

    return ws_error(400, "Can't create this note")


@login_required
def note_delete(user, data):

    if user.note_delete(data['note_id']):
        return ws_callback()

    return ws_error(400, 'Note could not be deleted')


@login_required
def note_get_list(user, data=None):

    notes = user.note_list_get()
    return ws_callback(notes)


@login_required
def item_add(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return ws_error(404, "Missing note")

    item = note.item_add(data['name'], data['description'])
    if item:
        return ws_callback(note.serialize())

    return ws_error(400, "Can't create new item")


@login_required
def item_delete(user, data):

    note = user.note_get(data['note_id'])

    if not note:
        return ws_error(404, "Missing note")

    if note.item_del(data['item_id']):
        return ws_callback()

    return ws_error(400, "Can't delete item")


@login_required
def item_mark(user, data):

    note = user.note_get(data['note_id'])

    if note.item_mark(data['item_id'], data['status']):
        return ws_callback()

    return ws_error(400, "Can't change status")


@login_required
def note_share(user, data):
    from apps.notes.exceptions import NoteShareException

    user2 = get_user_by_id(data['user_id'])

    if not user2:
        return ws_error(404, 'User not found')

    try:
        if user.share(data['note_id'], user2):
            return ws_callback()
    except NoteShareException:
        return ws_error(400, "Can't share note for this user")


@login_required
def note_archive(user, data):

    if user.note_archive(data['note_id'], data['status']):
        return ws_callback()

    return ws_error(400, "Can't" + ('' if data['status'] else 'un') + 'archive note')
