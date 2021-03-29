import datetime

import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs
from data.news import News

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({'jobs': [item.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished')
    )
        for item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators',
                                     'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'collaborators', 'start_date', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if request.json.get('id'):
        if db_sess.query(Jobs).filter(Jobs.id == int(request.json['id'])).first():
            return jsonify({'error': 'Id already exists'})
    job = Jobs(
        job=request.json['job'],
        work_size=int(request.json['work_size']),
        collaborators=request.json['collaborators'],
        start_date=datetime.datetime.strptime(
            request.json['start_date'], '%d-%m-%y').date(),
        is_finished=request.json['is_finished'],
        team_leader=int(request.json['team_leader'])
    )
    if request.json.get('id'):
        job.id = int(request.json['id'])
    if request.json.get('end_date'):
        job.end_date = datetime.datetime.strptime(
            request.json['end_date'], '%d-%m-%y').date()
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['PUT'])
def redact_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif not type(request.json['id']) == int:
        return jsonify({'error': 'Id should be integer'})

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(
        Jobs.id == int(request.json['id'])).first()
    if not job:
        return jsonify({'error': f'Id <{request.json["id"]}> not found'})
    try:
        job.team_leader = int(request.json['team_leader'])
        job.job = request.json['job']
        job.work_size = int(request.json['work_size'])
        job.collaborators = request.json['collaborators']
        job.start_date = datetime.datetime.strptime(
            request.json['start_date'], '%d-%m-%y').date()
        job.is_finished = request.json['is_finished']
        if request.json.get('end_date'):
            job.end_date = datetime.datetime.strptime(
                request.json['end_date'], '%d-%m-%y').date()
    except Exception:
        return jsonify({'error': 'Convert value Error'})
    db_sess.commit()

    return jsonify({'success': 'OK'})
