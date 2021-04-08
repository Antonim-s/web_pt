import datetime
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from flask_restful import reqparse
from data.parserfortrain import parser
from data.applications import Application


def abort_if_aplic_not_found(aplic_id):
    session = db_session.create_session()
    apl = session.query(Application).get(aplic_id)
    if not apl:
        abort(404, message=f"apliccation {aplic_id} not found")


class AplicResource(Resource):
    def get(self, aplic_id):
        abort_if_aplic_not_found(aplic_id)
        session = db_session.create_session()
        apl = session.query(Application).get(aplic_id)
        return jsonify({'aplic': apl.to_dict(
            only=('id', 'sostav', 'podgotovka', 'about', 'user_id'))})

    def delete(self, aplic_id):
        abort_if_aplic_not_found(aplic_id)
        session = db_session.create_session()
        apl = session.query(Application).get(aplic_id)
        session.delete(apl)
        session.commit()
        return jsonify({'success': 'OK'})


class AplicListResource(Resource):
    def get(self):
        session = db_session.create_session()
        apl = session.query(Application).all()
        return jsonify({'aplic': [item.to_dict(
            only=('id', 'sostav', 'podgotovka', 'about', 'user_id'))
            for item in apl]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        apl = Application(
            sostav=args['sostav'],
            podgotovka=args['podgotovka'],
            about=args['about'],
            user_id=int(args['user_id'])
        )
        session.add(apl)
        session.commit()
        return jsonify({'success': 'OK'})
