from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('category', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('content', required=False)
parser.add_argument('user_id', required=True)
