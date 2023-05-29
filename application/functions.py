from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
import datetime as d
import string





# checking for valid admin code
def match(code):
    # admin = Admin.query.filter_by(a_id = code[:4]).first()
    # if not admin:
    #     return False
    # if code != admin.a_id+admin.password:
    #     return False
    # return True
    admin = Admin.query.filter_by(a_id = code[:4]).first()
    if not admin:
        return False
    if code[4:] != encode(admin.password):
        return False
    return True


# cheching for valid member code
def match2(code):
    # member = Member.query.filter_by(m_id = code[:5]).first()
    # print(member.m_id+member.password)
    # if not member:
    #     return False
    # if code != member.m_id+member.password:
    #     return False
    # return True
    member = Member.query.filter_by(m_id = code[:5]).first()
    if not member:
        return False
    if code[5:] != encode(member.password):
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
        if q in book.isbn or q.lower() in book.title.lower():
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


# encode password
def encode(password):
    up = list(string.ascii_uppercase)
    lw = list(string.ascii_lowercase)
    di = list(string.digits)
    sp = list(string.punctuation)
    uplw = string.ascii_uppercase + string.ascii_lowercase

    new = ""
    for p in password:
        if p in up:
            new += lw[(up.index(p) + 11)%26]
            continue

        elif p in lw:
            new += di[(lw.index(p) + 7)%10]
            continue
        
        elif p in di:
            new += uplw[(di.index(p) + 13)%17]
            continue
        
        elif p in sp:
            new += uplw[(sp.index(p) + 29)%43]
        
        else:
            new += "x"
    return new



