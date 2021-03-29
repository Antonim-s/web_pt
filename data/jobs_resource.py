import datetime
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from flask_restful import reqparse
from data.jobs import Jobs
from data.parserforjob import parser



def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Jobs {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            id=int(args['job_id']),
            team_leader=int(args['team_leader']),
            job=args['job'],
            work_size=int(args['work_size']),
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        if args['start_date']:
            job.start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%y').date()
        if args['end_date']:
            job.end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%y').date()

        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})