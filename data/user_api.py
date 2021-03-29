import datetime

import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

from data.users import User

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({'users': [item.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email')
    )
        for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if request.json.get('id'):
        if db_sess.query(User).filter(User.id == int(request.json['id'])).first():
            return jsonify({'error': 'Id already exists'})
    try:
        user = User(
            surname=request.json['surname'],
            name=request.json['name'],
            age=int(request.json['age']),
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email']
        )
        user.set_password(request.json['password'])
        db_sess.add(user)
        db_sess.commit()
    except Exception:
        return jsonify({'error': 'Convert value Error'})
    if request.json.get('id'):
        user.id = int(request.json['id'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['PUT'])
def redact_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    elif not type(request.json['id']) == int:
        return jsonify({'error': 'Id should be integer'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.id == int(request.json['id'])).first()
    if not user:
        return jsonify({'error': f'Id <{request.json["id"]}> not found'})
    try:
        user.surname = request.json['surname'],
        user.name = request.json['name'],
        user.age = int(request.json['age']),
        user.position = request.json['position'],
        user.speciality = request.json['speciality'],
        user.address = request.json['address'],
        user.email = request.json['email']
        db_sess.commit()

    except Exception:
        return jsonify({'error': 'Convert value Error'})
    db_sess.commit()

    return jsonify({'success': 'OK'})
