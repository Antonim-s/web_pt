from requests import get, post, delete
import datetime

print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/999').json())
# print(get('http://localhost:5000/api/v2/jobs/q').json())

print(post('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs', json={'job': 'test'}).json())  # не все поля
print(post('http://localhost:5000/api/v2/jobs', json={'job_id': 10, 'job': 'test', 'work_size': 1,
                                                      'team_leader': 2, 'collaborators': '1, 3',

                                                      'is_finished': True}).json())

print(delete('http://localhost:5000/api/v2/jobs/999').json())
# print(delete('http://localhost:5000/api/v2/jobs/10').json())
