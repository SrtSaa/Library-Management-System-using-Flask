from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *





# Admin dashboard
@app.route("/Admin/<string:code>/Dashboard",methods=["GET", "POST"])
def admin_home(code):
    if not match(code):
        return redirect("/unknown")

    if request.method == "GET":  
        admin = Admin.query.filter_by(a_id = code[:4]).first()
        return render_template("admin_home.html",name=admin.f_name,code = code)



# View all members
@app.route("/Admin/<string:code>/Members/all",methods=["GET", "POST"])
def member_all(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":  
        l = extract_member(0)
        return render_template("members.html",code = code,members=l,m=0)
    
    elif request.method == "POST":
        l = extract_member2(request.form['q'], 0)
        return render_template("members.html",code = code,members=l,m=0,r=1,val=request.form['q'])



# View all student members
@app.route("/Admin/<string:code>/Members/student",methods=["GET", "POST"])
def member_student(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":  
        l = extract_member(1)
        return render_template("members.html",code = code,members=l,m=1)
    
    elif request.method == "POST":
        l = extract_member2(request.form['q'], 1)
        return render_template("members.html",code = code,members=l,m=1,r=1,val=request.form['q'])



# View all faculty members
@app.route("/Admin/<string:code>/Members/faculty",methods=["GET", "POST"])
def member_faculty(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":  
        l = extract_member(2)
        return render_template("members.html",code = code,members=l,m=2)
    
    elif request.method == "POST":  
        l = extract_member2(request.form['q'], 2)
        return render_template("members.html",code = code,members=l,m=2,r=1,val=request.form['q'])



# View member details
@app.route("/Admin/<string:code>/Members/<string:MID>/<int:m>",methods=["GET", "POST"])
def member_detail(code, MID, m):
    if not match(code):
        return redirect("unknown")
    
    member = Member.query.filter_by(m_id=MID).first()
    issued = B_Issue.query.filter_by(m_id=MID).all()
    isbns = []
    titles = []

    for copies in issued:
        x = db.session.query(B_Copies.isbn).filter_by(b_id=copies.b_id).first()
        isbns.append(x[0])
    for i in isbns:
        x = db.session.query(Book.title).filter_by(isbn=i).first()
        titles.append(x[0])

    if member.roll != None:
        stu = Student.query.filter_by(roll=member.roll).first()
        return render_template("member_details.html",code=code,member=member,person=stu,f=0,m=m,titles=titles,issued=issued)
    else:
        fac = Faculty.query.filter_by(f_id=member.f_id).first()
        return render_template("member_details.html",code=code,member=member,person=fac,f=1,m=m,titles=titles,issued=issued)
    


# Update member details
@app.route("/Admin/<string:code>/Members/<string:MID>/<int:m>/update",methods=["GET", "POST"])
def update_member_details(code,MID,m):
    if not match(code):
        return redirect("unknown")
    member = Member.query.filter_by(m_id=MID).first()
    if request.method == "GET":  
        if member.roll != None:
            stu = Student.query.filter_by(roll=member.roll).first()
            return render_template("member_details.html",code=code,member=member,person=stu,f=0,m=m,k=1)
        else:
            fac = Faculty.query.filter_by(f_id=member.f_id).first()
            return render_template("member_details.html",code=code,member=member,person=fac,f=1,m=m,k=1)
    elif request.method == "POST":
        member.password = request.form["fpass"]
        db.session.add(member)
        db.session.commit()
        return redirect("/Admin/"+code+"/Members/"+MID+"/"+str(m))



# Submit the book from member details
@app.route("/Admin/<string:code>/Members/<string:MID>/<int:m>/<string:BID>/submit",methods=["GET", "POST"])
def book_submit(code,MID,m,BID):
    if not match(code):
        return redirect("unknown")

    submit(MID,BID)

    return redirect("/Admin/"+code+"/Members/"+MID+"/"+str(m))



# Clear fine from member details
@app.route("/Admin/<string:code>/Members/<string:MID>/<string:m>/clear_fine",methods=["GET", "POST"])
def clear_fine(code,MID,m):
    if not match(code):
        return redirect("unknown")
    mem = Member.query.get(MID)
    mem.fine = 0
    db.session.add(mem)
    db.session.commit()

    if len(m)>5:
        return redirect("/Admin/"+code+"/Books/"+m+"/assign/Members/"+MID)
    
    return redirect("/Admin/"+code+"/Members/"+MID+"/"+m)



# Remove Member
@app.route("/Admin/<string:code>/Members/<string:MID>/<int:m>/Remove",methods=["GET", "POST"])
def remove_member(code,MID,m):
    if not match(code):
        return redirect("unknown")

    mem = mem = Member.query.get(MID)
    db.session.delete(mem)
    db.session.commit()
    if m==0:
        return redirect("/Admin/"+code+"/Members/all")
    elif m==1:
        return redirect("/Admin/"+code+"/Members/student")
    elif m==2:
        return redirect("/Admin/"+code+"/Members/faculty")



# Add Member
@app.route("/Admin/<string:code>/Members/add_member",methods=["GET", "POST"])
def add_member(code):
    if not match(code):
        return redirect("unknown")
    
    mem = Member.query.all()
    MID = mem[-1].m_id
    MID = str(int(MID[1:]) + 1)
    MID = 'M'+'0'*(4-len(MID))+MID

    if request.method == "GET":  
        return render_template("add_member.html",MID=MID,code=code,f=-1)
    

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
            return render_template("add_member.html",MID=MID,code=code,f=0,fid=fid,email=email,pw=pw,cpw=cpw,r=r)
        
        if r==0:
            id = Student.query.filter_by(roll=request.form["fid"]).first()
            member = Member.query.filter_by(roll=request.form["fid"]).first()
        else:
            id = Faculty.query.filter_by(f_id=request.form["fid"]).first()
            member = Member.query.filter_by(f_id=request.form["fid"]).first()
        
        if member:
            return render_template("add_member.html",MID=MID,code=code,f=3,fid=fid,email=email,pw=pw,cpw=cpw,r=r)
        
        if id == None:
            return render_template("add_member.html",MID=MID,code=code,f=1,fid=fid,email=email,pw=pw,cpw=cpw,r=r)
        else:
            if id.email != request.form["femail"]:
                return render_template("add_member.html",MID=MID,code=code,f=2,fid=fid,email=email,pw=pw,cpw=cpw,r=r)
            
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
                return redirect("/Admin/"+code+"/Members/"+request.form["fmid"]+"/0")




