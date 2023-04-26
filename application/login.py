from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *





# Log in page
@app.route("/",methods=["GET", "POST"])
def home():
    AE = UE = "Enter Email ID"
    AP = UP = "Enter Password"

    if request.method == "GET":  
        return render_template("index.html",AE=AE,UE=UE,AP=AP,UP=UP)
    
    elif request.method == "POST":
        if request.form['type'] == "Admin":
            present = Admin.query.filter_by(email = request.form["femail"]).first()
            
            if present:
                if present.password != request.form["fpass"]:
                    return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=1)
                else:
                    # return redirect("/Admin/"+present.a_id+present.password+"/Dashboard")
                    return redirect("/Admin/"+present.a_id+encode(present.password)+"/Dashboard")
            
            else:
                return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=0)
        

        elif request.form['type'] == "User":
            email = request.form["femail"]
            type = request.form["ftype"]
            pw = request.form["fpass"]
            
            if type=='Student':
                r=0
            else:
                r=1
            
            present = Member.query.filter_by(email = email).first()
            
            if present:
                if r==0 and present.type != 'Student':
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=0,r=r)
                elif r==1 and present.type != 'Faculty':
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=0,r=r)

                elif present.password != pw:
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=1,r=r)
                else:
                    # return redirect("/Member/"+present.m_id+present.password+"/Dashboard")
                    return redirect("/Member/"+present.m_id+encode(present.password)+"/Dashboard")
                
            else:
                if r==0:
                    user = Student.query.filter_by(email = email).first()
                else:
                    user = Faculty.query.filter_by(email = email).first()
                
                if user:
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=2,r=r)
                else:
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=0,r=r)


# Register new member
@app.route("/Add_member",methods=["GET", "POST"])
def register_member():
    mem = Member.query.all()
    MID = mem[-1].m_id
    MID = str(int(MID[1:]) + 1)
    MID = 'M'+'0'*(4-len(MID))+MID

    if request.method == "GET":  
        return render_template("add_member.html",MID=MID,u=1,f=-1)
    
    elif request.method == "POST":  
        member = Member.query.filter_by(m_id=request.form["fmid"]).first()
        type = request.form["ftype"]
        if type == 'Student':
            r = 0
        else:
            r = 1
        fid = request.form["fid"]
        email = request.form["femail"]
        pw = request.form["fpass"]
        cpw = request.form["fcpass"]
        if member:
            return render_template("add_member.html",MID=MID,f=0,fid=fid,email=email,pw=pw,cpw=cpw,r=r,u=1)
        if r==0:
            id = Student.query.filter_by(roll=request.form["fid"]).first()
            member = Member.query.filter_by(roll=request.form["fid"]).first()
        else:
            id = Faculty.query.filter_by(f_id=request.form["fid"]).first()
            member = Member.query.filter_by(f_id=request.form["fid"]).first()
        if member:
            return render_template("add_member.html",MID=MID,f=3,fid=fid,email=email,pw=pw,cpw=cpw,r=r,u=1)
        if id == None:
            return render_template("add_member.html",MID=MID,f=1,fid=fid,email=email,pw=pw,cpw=cpw,r=r,u=1)
        else:
            if id.email != request.form["femail"]:
                return render_template("add_member.html",MID=MID,f=2,fid=fid,email=email,pw=pw,cpw=cpw,r=r,u=1)
            else:
                member = Member()
                member.m_id = request.form["fmid"]
                member.type = type
                if r==0:
                    member.roll = fid
                else:
                    member.f_id = fid
                member.email = email
                member.password = pw
                member.max_issue_left = 5
                member.fine = 0
                db.session.add(member)
                db.session.commit()
                return redirect("/")

