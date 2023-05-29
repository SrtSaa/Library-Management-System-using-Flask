from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *





# Admin profile
@app.route("/Admin/<string:code>/Profile",methods=["GET", "POST"])
def view_profile(code):
    if not match(code):
        return redirect("/unknown")
    
    if request.method == "GET":  
        admin = Admin.query.filter_by(a_id=code[:4]).first()
        return render_template("details.html",code=code,person=admin,u=1)



# Update profile
@app.route("/Admin/<string:code>/Profile/update",methods=["GET", "POST"])
def update_profile(code):
    if not match(code):
        return redirect("/unknown")
    
    admin = Admin.query.filter_by(a_id=code[:4]).first ()
    if request.method == "GET":  
        return render_template("details.html",code=code,person=admin,u=1,e=1)
    
    if request.method == "POST":  
        admin.password = request.form['fpass']
        db.session.add(admin)
        db.session.commit()
        # code = admin.a_id+request.form['fpass']
        code = admin.a_id+encode(request.form['fpass'])
        return redirect("/Admin/"+code+"/Profile")




