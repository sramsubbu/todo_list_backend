from flask import jsonify, request, abort

from todo_app import app
from todo_app.models import CheckList, Item
from todo_app.db import Session


@app.route('/')
@app.route('/index/')
def api_index():
    values = Session.query(CheckList).all()
    values = [row_to_dict(row) for row in values]
    response = {'checklists': values}
    return jsonify(response)


@app.route('/add_list/', methods= ['POST'])
def api_add_list():
    if 'list_name' not in request.form:
        return build_response('Require parameter "list_name" to process this request')
    list_name = request.form['list_name']
    obj = CheckList(name=list_name)
    Session.add(obj)
    Session.commit()
    return build_response("Added checklist successfully.", checklist_id =obj.id)


@app.route('/delete_list/', methods=['POST'])
def api_delete_list():
    if 'list_id' not in request.form:
        return build_response('Require "list_id" parameter')
    list_id = int(request.form['list_id'])
    checklist = Session.query(CheckList).filter_by(id=list_id).first()
    Session.delete(checklist)
    Session.commit()
    return build_response("Deleted the checklist successfully.")


@app.route('/list/', methods=["GET"])
def api_get_list_items():
    if 'list_id' not in request.form:
        print(request.form)
        return build_response('Require "list_id" parameter')
    list_id = int(request.form['list_id'])
    checklist = Session.query(CheckList).filter_by(id=list_id).first()
    items = checklist.item
    items = [row_to_dict(row) for row in items]
    return jsonify({"checklist": row_to_dict(checklist), "items": items})


@app.route('/list/add_item/', methods=["POST"])
def api_add_list_item():
    if 'list_id' not in request.form:
        return build_response("Require 'list_id' parameter")
    list_id = int(request.form['list_id'])
    checklist = Session.query(CheckList).filter_by(id=list_id).first()
    if 'item_name' not in request.form:
        return build_response("Require 'item_name' parameter")
    item_name = request.form['item_name']
    item = Item(name=item_name, checklist=checklist)
    Session.add(item)
    Session.commit()
    return build_response("Item added successfully.")


@app.route('/list/delete_item/', methods=['POST'])
def api_delete_list_item():
    list_id = int(get_form_param('list_id', request.form))
    checklist = Session.query(CheckList).filter_by(id=list_id).first()
    item_id = int(get_form_param('item_id', request.form))
    item = Session.query(Item).filter_by(id=item_id, checklist=checklist).first()
    Session.delete(item)
    Session.commit()
    return build_response('Item deleted successfully')


@app.route('/list/update_item/', methods=['POST'])
def api_update_list_item():
    list_id = int(get_form_param('list_id', request.form))
    checklist = Session.query(CheckList).filter_by(id=list_id).first()
    item_id = int(get_form_param('item_id', request.form))
    item = Session.query(Item).filter_by(id=item_id, checklist=checklist).first()
    task_status=bool(int(get_form_param('task_status', request.form)))
    item.task_completed = task_status
    Session.add(item)
    Session.commit()
    return build_response("Item modified successfully")


def build_response(message=None, status='Success', **kwargs):
    response = kwargs.copy()
    if message is not None:
        response['message'] = message
    response['status'] = status
    return jsonify(response)


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d
    # return {column.name: getattr(column.name, row) for column in row.__table__.columns}


def get_form_param(param_name, form_obj):
    if param_name not in form_obj:
        abort(404)
    value = form_obj[param_name]
    return value