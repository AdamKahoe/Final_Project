from flask_app import app

from flask_app.controllers import controllers_users, controllers_posts
from flask_app.models import models_post, models_user

if __name__=="__main__":
    app.run(debug=True)