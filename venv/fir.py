from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    intro = db.Column(db.Text, nullable=False)
    m_text=db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return 'Blog %r'%self.id
@app.route('/index')
@app.route('/')
def index():
    notes=Blog.query.all()
    notes=notes[::-1]
    return render_template('index.html',notes=notes)
@app.route('/about')
def about():
    a='QWERt'
    return render_template('about.html',zm=a)
@app.route('/adres')
def adres():
    names = [{'name': 'Олексій Масловський', 'e-mail': 'alexus450@gmail.com', 'cell number': '0973410024'},
             {'name': 'Ivan', 'email': '12354@gmail.com', 'call number': '0664297574'},
             {"name": "Антон Юксін", "e-mail": 'qpowertrain@gmail.com', "number": "06668*****"},
             {'name': 'Dennis', 'e-mail': 'bachynskyi.denys@pml.if.ua', 'phone-number': '3001113344'},
             {'name': 'Стефунін Арсен', 'email': 'stefunin.arsen@pml.if.ua', 'cell number': '+380672925255'}]
    return render_template('adres.html',dname=names)
@app.route('/article',methods=['POST','GET'])
def article():

    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        m_text = request.form['m_text']
        blog=Blog(title=title,intro=intro,m_text=m_text)
        try:
            db.session.add(blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'

    else:
        return render_template('article.html')
@app.route('/sign',methods=['POST','GET'])
def sign():
    if request.method=='POST':
         name=request.form['Name']
         password=request.form['Password']
         return name+password
    return render_template('sign.html')

@app.route('/info/<int:id>')
def info(id):
    m_info=Blog.query.get(id)
    return render_template('moreinfo.html', m_info=m_info)
@app.route('/info/<int:id>/del')
def del_s(id):
    d_s=Blog.query.get_or_404(id)
    try:
        db.session.delete(d_s)
        db.session.commit()
        return redirect('/')
    except:
        return 'error'
@app.route('/info/<int:id>/edit',methods=['POST','GET'])
def edit(id):
    e_t = Blog.query.get(id)
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        m_text = request.form['m_text']
        print(title)
        redirect('/')
    else:
        return render_template('editArt.html',title=e_t.title,intro=e_t.intro,m_text=e_t.m_text)

if __name__=='__main__':
    app.run(debug=True)
