from flask import render_template, request, redirect
from flask import current_app as app
from model import *
import string
import datetime as d


# checking for valid admin code
def match(code):
    admin = Admin.query.filter_by(a_id = code[:4]).first()
    if not admin:
        return False
    if code != admin.a_id+admin.password:
        return False
    return True
        
# extract the members
def extract_member(m):
    l = []
    if m==0:
        members = Member.query.all()
        for member in members:
            x = []
            if member.roll != None:
                q = db.session.query(Student.f_name,Student.l_name,Student.dept_code).filter_by(roll=member.roll).first()
            else:
                q = db.session.query(Faculty.f_name,Faculty.l_name,Faculty.dept_code).filter_by(f_id=member.f_id).first()
            x.extend([member.m_id,member.type,q[0]+" "+q[1],q[2],member.email])
            l.append(x)

    elif m==1:
        members = Member.query.filter_by(type='Student').all()
        for member in members:
            x = []
            q = db.session.query(Student.f_name,Student.l_name,Student.dept_code).filter_by(roll=member.roll).first()
            x.extend([member.m_id,member.type,q[0]+" "+q[1],q[2],member.email])
            l.append(x)
    
    else:
        members = Member.query.filter_by(type='Faculty').all()
        for member in members:
            x = []
            q = db.session.query(Faculty.f_name,Faculty.l_name,Faculty.dept_code).filter_by(f_id=member.f_id).first()
            x.extend([member.m_id,member.type,q[0]+" "+q[1],q[2],member.email])
            l.append(x)
    return l

# extract members based on search
def extract_member2(x,m):
    if m==0:
        mem = Member.query.all()
    elif m==1:
        mem = Member.query.filter_by(type='Student').all()
    else:
        mem = Member.query.filter_by(type='Faculty').all()
    l = []
    for m in mem:
        f = 0
        if x in m.m_id:
            f = 1
        else:
            if m.roll != None:
                q = db.session.query(Student.f_name,Student.l_name,Student.dept_code).filter_by(roll=m.roll).first()
            else:
                q = db.session.query(Faculty.f_name,Faculty.l_name,Faculty.dept_code).filter_by(f_id=m.f_id).first()
            if x.lower() in (q[0]+" "+q[1]).lower():
                y = []
                y.extend([m.m_id,m.type,q[0]+" "+q[1],q[2],m.email])
                l.append(y)
                continue
                
        if f==1:
            y = []
            if m.roll != None:
                q = db.session.query(Student.f_name,Student.l_name,Student.dept_code).filter_by(roll=m.roll).first()
            else:
                q = db.session.query(Faculty.f_name,Faculty.l_name,Faculty.dept_code).filter_by(f_id=m.f_id).first()
            y.extend([m.m_id,m.type,q[0]+" "+q[1],q[2],m.email])
            l.append(y)
    return l

# Extracting M+IDs who take copy of a particular book
def extract_mid(copies):
    mids = []
    for copy in copies:
        issue = B_Issue.query.filter_by(b_id=copy.b_id).first()
        if not issue:
            mids.append("None")
        else:
            mids.append(issue.m_id)
    return mids

# Submit Book
def submit(MID,BID):
    copy = B_Copies.query.get(BID)
    copy.assigned = "No"
    db.session.add(copy)
    issue = B_Issue.query.filter_by(m_id=MID,b_id=BID).first()
    mem = Member.query.get(MID)
    mem.max_issue_left += 1
    s = issue.dor
    l = list(map(int,s.split('-')))
    s = d.date(l[0],l[1],l[2])
    x = d.date.today()
    if x>s:
        l = str(x-s).split(' ')
        mem.fine = int(l[0])*2
    db.session.add(mem)
    db.session.delete(issue)
    db.session.commit()
    
    return copy.isbn

# extract the books
def extract_book(books):
    authors = []
    for book in books:
        x = book.f_author
        if book.s_author == None:
            authors.append(x)
            continue
        else:
            x += ", "+book.s_author
            if book.t_author == None:
                authors.append(x)
                continue
            else:
                x += ", "+book.t_author
        authors.append(x)

    return authors

# extract books based on search
def extract_book2(q):
    sbooks = []
    books = Book.query.all()
    for book in books:
        if q in book.isbn or q in book.title:
            sbooks.append(book)
            continue
        elif q.lower() in book.publisher.lower():
            sbooks.append(book)
            continue
        elif q.lower() in book.f_author.lower(): 
            sbooks.append(book)
            continue
        elif book.s_author != None and q.lower() in book.s_author.lower():
            sbooks.append(book)
            continue
        elif book.t_author != None and q.lower() in book.t_author.lower():
            sbooks.append(book)
            continue

    authors = extract_book(sbooks)
    return sbooks,authors








# Log in page
@app.route("/",methods=["GET", "POST"])
def home():
    AE = UE = "Enter Email ID"
    AP = UP = "Enter Password"
    if request.method == "GET":  
        return render_template("index.html",AE=AE,UE=UE,AP=AP,UP=UP)
    else:
        if request.form['type'] == "Admin":
            present = Admin.query.filter_by(email = request.form["femail"]).first()
            if present:
                if present.password != request.form["fpass"]:
                    return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=1)
                else:
                    return redirect("/Admin/"+present.a_id+present.password+"/Dashboard")
            else:
                return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=0)


# Admin dashboard
@app.route("/Admin/<string:code>/Dashboard",methods=["GET", "POST"])
def admin_home(code):
    if not match(code):
        return redirect("/unknown")

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

    l = extract_member(m)
    borrow = B_Issue.query.filter_by(m_id=MID).first()
    if borrow:
        return render_template("members.html",code = code,members=l,m=m,f=1,id=MID)
    mem = mem = Member.query.get(MID)
    if mem.fine != 0:
        return render_template("members.html",code = code,members=l,m=m,f=2,id=MID)
    db.session.delete(mem)
    db.session.commit()
    if m==0:
        return redirect("/Admin/"+code+"/Members/all")
    elif m==1:
        return redirect("/Admin/"+code+"/Members/student")
    else:
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
                return redirect("/Admin/"+code+"/Members/all")













# View Books
@app.route("/Admin/<string:code>/Books",methods=["GET", "POST"])
def view_books(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":
        books = Book.query.all()
        authors=extract_book(books)
        return render_template("books.html",code=code,books=books,authors=authors,a=1)
    
    elif request.method == "POST":
        books,authors = extract_book2(request.form['q'])
        return render_template("books.html",code = code,books=books,authors=authors,a=1,r=1,val=request.form['q'])
    


# Remove Book
@app.route("/Admin/<string:code>/Book/remove",methods=["GET", "POST"])
def remove_book(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "POST":
        book = Book.query.filter_by(isbn=request.form['isbn']).first()
        db.session.delete(book)
        db.session.commit()
        return redirect("/Admin/"+code+"/Books")



# View Book Details
@app.route("/Admin/<string:code>/Books/<string:isbn>",methods=["GET", "POST"])
def book_details(code,isbn):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":
        if code[0]=="A":
            a=1
        book = Book.query.filter_by(isbn=isbn).first()
        copies = B_Copies.query.filter_by(isbn=isbn).all()
        mids = extract_mid(copies)

        return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,a=a)



# Remove Book Copies
@app.route("/Admin/<string:code>/Book/copy/remove",methods=["GET", "POST"])
def copy_remove(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "POST":
        bid = request.form['bid']
        copy = B_Copies.query.filter_by(b_id=bid).first()
        isbn = copy.isbn
        db.session.delete(copy)
        book = Book.query.filter_by(isbn=isbn).first()
        book.copies -= 1
        db.session.add(book)
        db.session.commit()

        return redirect("/Admin/"+code+"/Books/"+isbn)



# Assign Book Copies
@app.route("/Admin/<string:code>/Book/assign",methods=["GET", "POST"])
def assign_copy(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "POST":
        isbn = request.form['isbn']
        bid = request.form['bid']
        k = request.form['k']

        book = Book.query.filter_by(isbn=isbn).first()
        copies = B_Copies.query.filter_by(isbn=isbn).all()
        mids = extract_mid(copies)

        if k == "1":  
            return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=2)
        
        elif k == "2":
            mem = Member.query.filter_by(m_id=request.form['mid']).first()
            if not mem:
                return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=3,mid=request.form['mid'])
            
            if mem.max_issue_left == 0:
                return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=7,mid=request.form['mid'])

            books = B_Issue.query.filter_by(m_id=request.form['mid']).all()
            for b in books:
                s = b.dor
                l = list(map(int,s.split('-')))
                s = d.date(l[0],l[1],l[2])
                x = d.date.today()

                if x>s:
                    return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=4,mid=request.form['mid'])
                
                if b.b_id[:-1] == bid[:-1]:
                    return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=6,mid=request.form['mid'])

            if mem.fine > 0:
                return render_template("book_details.html",code=code,book=book,copies=copies,mids=mids,bid=bid,a=5,mid=request.form['mid'])
            
            issue = B_Issue()
            issue.m_id = request.form['mid']
            issue.b_id = bid
            issue.doi = str(d.date.today())
            issue.dor = str(d.date.today()+d.timedelta(days=14))
            db.session.add(issue)
            mem.max_issue_left -= 1
            db.session.add(mem)
            copy = B_Copies.query.filter_by(b_id=bid).first()
            copy.assigned = 'Yes'
            db.session.add(copy)
            db.session.commit()

            return redirect("/Admin/"+code+"/Books/"+isbn)



# View member details from book details due to assign error
@app.route("/Admin/<string:code>/Books/<string:isbn>/assign/Members/<string:MID>",methods=["GET", "POST"])
def view_member(code,isbn,MID):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":

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
            return render_template("member_details.html",code=code,member=member,person=stu,f=0,r=1,titles=titles,issued=issued,isbn=isbn)
        
        else:
            fac = Faculty.query.filter_by(f_id=member.f_id).first()
            return render_template("member_details.html",code=code,member=member,person=fac,f=1,r=1,titles=titles,issued=issued,isbn=isbn)
    


# Submit the book due to assign error
@app.route("/Admin/<string:code>/Members/book/submit",methods=["GET", "POST"])
def book_submit_for_assign_error(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "POST": 
        MID = request.form['MID']
        m = request.form['x']
        BID = request.form['BID']
        
        isbn = submit(MID,BID)
        if m=='1':
            return redirect("/Admin/"+code+"/Books/"+isbn)
        
        elif m=='2':
            return redirect("/Admin/"+code+"/Books/"+request.form['isbn']+"/assign/Members/"+MID)



# Add Book Copies
@app.route("/Admin/<string:code>/Book/add_copies",methods=["GET", "POST"])
def add_copies(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "POST":
        isbn = request.form['isbn']
        k = request.form['k']
        book = Book.query.filter_by(isbn=isbn).first()

        if k=='1':
            return render_template("book_details.html",code=code,book=book,a=8)
        
        elif k=='2':
            x = int(request.form['fcp'])
            alpha = list(string.ascii_uppercase)
            i = book.copies
            for k in range(x):
                copy = B_Copies()
                copy.b_id = isbn + alpha[i]
                copy.isbn = isbn
                copy.assigned = 'No'
                i += 1
                db.session.add(copy)
            book.copies += x
            db.session.add(book)
            db.session.commit()

            return redirect("/Admin/"+code+"/Books/"+isbn)



# Add New Book
@app.route("/Admin/<string:code>/Books/add",methods=["GET", "POST"])
def add_book(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":
        return render_template('add_book.html',code=code)
    
    elif request.method == "POST":

        i=request.form['fisbn']
        t=request.form['ftitle']
        p=request.form['fpub']
        y=int(request.form['fyear'])
        fa=request.form['ffau']
        s=request.form['fsau']
        th=request.form['ftau']
        c=int(request.form['fcp'])

        book = Book.query.filter_by(isbn=request.form['fisbn']).first()
        if book:
            return render_template('add_book.html',code=code,f=1,i=i,t=t,p=p,y=y,fa=fa,s=s,th=th,c=c)
        
        book = Book()
        book.isbn = i
        book.title = t
        book.publisher = p
        book.year = y
        book.f_author = fa
        

        if len(s.strip())==0:
            book.s_author = None
        if len(th.strip())==0:
            book.th_author = None
        
        book.copies = c
        alpha = list(string.ascii_uppercase)
        j = 0
        for k in range(c):
            copy = B_Copies()
            copy.b_id = i + alpha[j]
            copy.isbn = i
            copy.assigned = 'No'
            j += 1
            db.session.add(copy)
        db.session.add(book)
        db.session.commit()
        
        return redirect("/Admin/"+code+"/Books/"+i)

















