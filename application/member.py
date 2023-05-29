from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *





# Member dashboard
@app.route("/Member/<string:code>/Dashboard",methods=["GET", "POST"])
def member_home(code):
    if not match2(code):
        return redirect("/unknown")

    if request.method == "GET":  
        member = Member.query.filter_by(m_id = code[:5]).first()
        if member.roll!=None:
            per = Student.query.filter_by(roll=member.roll).first()
        else:
            per = Faculty.query.filter_by(f_id=member.f_id).first()
        return render_template("member_home.html",name=per.f_name,code = code)



# View Books
@app.route("/Member/<string:code>/Books",methods=["GET", "POST"])
def view_Books(code):
    if not match2(code):
        return redirect("unknown")
    
    if request.method == "GET":
        books = Book.query.all()
        authors=extract_book(books)
        return render_template("books.html",code=code,books=books,authors=authors,a=0)
    
    elif request.method == "POST":
        books,authors = extract_book2(request.form['q'])
        return render_template("books.html",code = code,books=books,authors=authors,a=0,r=1,val=request.form['q'])



# View Book Details
@app.route("/Member/<string:code>/Books/<string:isbn>",methods=["GET", "POST"])
def book_Details(code,isbn):
    if not match2(code):
        return redirect("unknown")
    
    if request.method == "GET":
        if code[0]=="M":
            a=0
        book = Book.query.filter_by(isbn=isbn).first()
        copies = B_Copies.query.filter_by(isbn=isbn).all()
        mids = extract_mid(copies)

        return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,a=a)



# Member profile
@app.route("/Member/<string:code>/Profile",methods=["GET", "POST"])
def view_Profile(code):
    if not match2(code):
        return redirect("/unknown")
    
    if request.method == "GET":  
        member = Member.query.filter_by(m_id=code[:5]).first()
        issued = B_Issue.query.filter_by(m_id=code[:5]).all()
        isbns = []
        titles = []
        for copies in issued:
            x = db.session.query(B_Copies.isbn).filter_by(b_id=copies.b_id).first()
            isbns.append(x[0])
        for i in isbns:
            x = db.session.query(Book.title).filter_by(isbn=i).first()
            titles.append(x[0])

        if member.roll!=None:
            per = Student.query.filter_by(roll=member.roll).first()
            return render_template("details.html",code=code,member=member,person=per,titles=titles,issued=issued,u=2)
        else:
            per = Faculty.query.filter_by(f_id=member.f_id).first()
            return render_template("details.html",code=code,member=member,person=per,titles=titles,issued=issued,u=3)



# Update profile
@app.route("/Member/<string:code>/Profile/update",methods=["GET", "POST"])
def update_Profile(code):
    if not match2(code):
        return redirect("/unknown")
    
    member = Member.query.filter_by(m_id=code[:5]).first ()
    if request.method == "GET":  
        if member.roll!=None:
            per = Student.query.filter_by(roll=member.roll).first()
            return render_template("details.html",code=code,member=member,person=per,u=2,e=1)
        else:
            per = Faculty.query.filter_by(f_id=member.f_id).first()
            return render_template("details.html",code=code,member=member,person=per,u=3,e=1)

    
    if request.method == "POST":  
        member.password = request.form['fpass']
        db.session.add(member)
        db.session.commit()
        # code = member.m_id+request.form['fpass']
        code = member.m_id+encode(request.form['fpass'])
        return redirect("/Member/"+code+"/Profile")



