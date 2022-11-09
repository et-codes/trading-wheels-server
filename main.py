import os
import sys
import trades
import users
import views
from database import db
from dotenv import load_dotenv
from flask import Flask
from models import User, Trade


# Initialize application
load_dotenv()
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


# Set up database
with app.app_context():
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'rebuild':
        # Recreate tables if 'rebuild' argument used on command line
        print('Rebuilding database tables...')
        db.drop_all()
        db.create_all()
        sys.exit(0)
    else:
        # Create tables if they don't already exist
        db.create_all()


# Set up routes
## User endpoints
app.add_url_rule('/user', view_func=users.create_user, methods=['POST'])
app.add_url_rule('/user', view_func=users.delete_user, methods=['DELETE'])
app.add_url_rule('/user/<username>', view_func=users.check_user)
app.add_url_rule('/user/login', view_func=users.login, methods=['POST'])
app.add_url_rule('/user/logout/<username>', view_func=users.logout)

## Trading endpoints
app.add_url_rule('/trades/<user_id>', view_func=trades.get_portfolio)
app.add_url_rule('/trades', view_func=trades.trade, methods=['POST'])

## Home page
@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
