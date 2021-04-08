from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('sostav', required=True)
parser.add_argument('dur', required=True, type=int)
parser.add_argument('date', required=True)
parser.add_argument('user_id', required=True)
