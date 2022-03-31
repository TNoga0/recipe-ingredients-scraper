from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

# this below is only temporary
import pickle
fh = open("../processed_recipes", "rb")
recipes = pickle.load(fh)
fh.close()
# end temporary

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(Config)


class Scrape(Resource):

    def get(self):
        # TODO insert scraping here
        return {"Status": "OK"}, 200


class UpdateDatabase(Resource):

    def post(self):
        pass

    def get(self):
        return recipes, 200


api.add_resource(UpdateDatabase, "/update_db")

if __name__ == '__main__':
    app.run(debug=True)
