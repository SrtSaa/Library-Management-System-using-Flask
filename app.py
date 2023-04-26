from flask import render_template, request
from flask import Flask
from application.model import *



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lis.sqlite3'
db.init_app(app)
app.app_context().push()



# from controllers import *
from application.login import *
from application.admin_Mem import *
from application.admin_Book import *
from application.admin_Profile import *
from application.member import *




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False,host="0.0.0.0")
