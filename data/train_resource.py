import datetime
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from flask_restful import reqparse
from data.parserfortrain import parser
from data.train import Train


def abort_if_train_not_found(train_id):
    session = db_session.create_session()
    tr = session.query(Train).get(train_id)
    if not tr:
        abort(404, message=f"Trains {train_id} not found")


class TrainResource(Resource):
    def get(self, train_id):
        abort_if_train_not_found(train_id)
        session = db_session.create_session()
        train = session.query(Train).get(train_id)
        return jsonify({'train': train.to_dict(
            only=('id', 'sostav', 'dur', 'date', 'user_id'))})

    def delete(self, train_id):
        abort_if_train_not_found(train_id)
        session = db_session.create_session()
        train = session.query(Train).get(train_id)
        session.delete(train)
        session.commit()
        return jsonify({'success': 'OK'})


class TrainListResource(Resource):
    def get(self):
        session = db_session.create_session()
        train = session.query(Train).all()
        return jsonify({'train': [item.to_dict(
            only=('id', 'sostav', 'dur', 'date', 'user_id'))
            for item in train]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        train = Train(
            sostav=args['sostav'],
            dur=int(args['dur']),
            user_id=args['user_id']
        )
        if args['date']:
            train.date = datetime.datetime.strptime(args['start_date'], '%d-%m-%y %H:%M').date()

        session.add(train)
        session.commit()
        return jsonify({'success': 'OK'})