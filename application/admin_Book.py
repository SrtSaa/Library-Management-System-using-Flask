from flask import render_template, request, redirect
from flask import current_app as app
import string
import datetime as d
from application.functions import *
from application.model import *





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
            copies = B_Copies.query.filter_by(isbn=isbn).all()
            for copy in copies:
                d = copy.b_id[-1]
                alpha.remove(d)
            i = 0
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



# Overdue books
@app.route("/Admin/<string:code>/Books/overdue",methods=["GET", "POST"])
def overdue(code):
    if not match(code):
        return redirect("unknown")
    
    if request.method == "GET":
        issued = B_Issue.query.all()
        issues = []
        for issue in issued:
            s = issue.dor
            l = list(map(int,s.split('-')))
            s = d.date(l[0],l[1],l[2])
            x = d.date.today()
            if x>s:
                issues.append(issue)
        
        names = []
        for copy in issues:
            x = db.session.query(B_Copies.isbn).filter_by(b_id=copy.b_id).first()
            n = db.session.query(Book.title).filter_by(isbn=x[0]).first()
            names.append(n[0])
        
        return render_template("overdue.html",code=code,issues=issues,names=names)
    
    elif request.method == "POST":
        mid = request.form['mid']
        member = Member.query.filter_by(m_id=mid).first()
        issued = B_Issue.query.filter_by(m_id=mid).all()
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
            return render_template("member_details.html",code=code,member=member,person=per,titles=titles,issued=issued,f=0,k=2)
        else:
            per = Faculty.query.filter_by(f_id=member.f_id).first()
            return render_template("member_details.html",code=code,member=member,person=per,titles=titles,issued=issued,f=1,k=2)



