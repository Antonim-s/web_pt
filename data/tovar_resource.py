import datetime
import os

from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from flask_restful import reqparse
from data.parserfortrain import parser
from data.tovari import Tovar


def abort_if_tovar_not_found(tovar_id):
    session = db_session.create_session()
    tovar = session.query(Tovar).get(tovar_id)
    if not tovar:
        abort(404, message=f"tovar {tovar_id} not found")


class TovarResource(Resource):
    def get(self, tovar_id):
        abort_if_tovar_not_found(tovar_id)
        session = db_session.create_session()
        tovar = session.query(Tovar).get(tovar_id)
        return jsonify({'tovar': tovar.to_dict(
            only=('id', 'category', 'price', 'img', 'content', 'user_id'))})

    def delete(self, tovar_id):
        abort_if_tovar_not_found(tovar_id)
        session = db_session.create_session()
        tovar = session.query(Tovar).get(tovar_id)
        if tovar.img:
            os.remove(tovar.img)
        session.delete(tovar)
        session.commit()
        return jsonify({'success': 'OK'})


class TovarListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tovar = session.query(Tovar).all()
        return jsonify({'tovar': [item.to_dict(
            only=('id', 'category', 'price', 'img', 'content', 'user_id'))
            for item in tovar]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        tovar = Tovar(
            category=args['category'],
            price=int(args['price']),
            about=args['about'],
            user_id=args['user_id']
        )
        session.add(tovar)
        session.commit()
        return jsonify({'success': 'OK'})
