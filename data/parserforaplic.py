from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('sostav', required=True)
parser.add_argument('podgotovka', required=True, type=int)
parser.add_argument('about', required=False)
parser.add_argument('user_id', required=True)
