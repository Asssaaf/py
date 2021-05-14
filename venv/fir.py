from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager,login_user,login_required,logout_user,UserMixin
myapp=Flask(__name__)
myapp.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
myapp.config['SECRET_KEY']='q0w9e8r7'
db=SQLAlchemy(myapp)
my_login=LoginManager()
my_login.init_app(myapp)
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(40), nullable=False)
class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    intro = db.Column(db.Text, nullable=False)
    m_text=db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return 'Blog %r'%self.id
@my_login.user_loader
def loader(id):

    return User.query.get(id)
@myapp.route('/login')
def log_in():
    user=User.query.filter_by(name='First').first()
    login_user(user)
    return 'Logged'
@myapp.route('/logout')
def log_out():
    user = User.query.filter_by(name='First').first()
    log_out()
    return 'Logged out'
@myapp.route('/index')
@myapp.route('/')
def index():
    notes=Blog.query.all()
    notes=notes[::-1]
    return render_template('index.html',notes=notes)
@myapp.route('/about')
def about():
    a='QWERt'
    return render_template('about.html',zm=a)
@myapp.route('/adres')
def adres():
    names = [{'name': 'Олексій Масловський', 'e-mail': 'alexus450@gmail.com', 'cell number': '0973410024'},
             {'name': 'Ivan', 'email': '12354@gmail.com', 'call number': '0664297574'},
             {"name": "Антон Юксін", "e-mail": 'qpowertrain@gmail.com', "number": "06668*****"},
             {'name': 'Dennis', 'e-mail': 'bachynskyi.denys@pml.if.ua', 'phone-number': '3001113344'},
             {'name': 'Стефунін Арсен', 'email': 'stefunin.arsen@pml.if.ua', 'cell number': '+380672925255'}]
    return render_template('adres.html',dname=names)
@myapp.route('/article',methods=['POST','GET'])
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
@myapp.route('/sign',methods=['POST','GET'])
def sign():
    if request.method=='POST':
         user=User.query.filter_by( name=request.form['Name'])
         password=request.form['Password']
         return password
    return render_template('sign.html')

@myapp.route('/info/<int:id>')
def info(id):
    m_info=Blog.query.get(id)
    return render_template('moreinfo.html', m_info=m_info)
@myapp.route('/info/<int:id>/del')
def del_s(id):
    d_s=Blog.query.get_or_404(id)
    try:
        db.session.delete(d_s)
        db.session.commit()
        return redirect('/')
    except:
        return 'error'
@myapp.route('/info/<int:id>/edit',methods=['POST','GET'])
def edit(id):
    e_t = Blog.query.get(id)
    if request.method == 'POST':

        try:
            e_t.title = request.form['title']
            e_t.intro = request.form['intro']
            e_t.m_text = request.form['m_text']
            db.session.commit()
        except:
            return redirect('/')
        return redirect('/')

    return render_template('editArt.html',title=e_t.title,intro=e_t.intro,m_text=e_t.m_text)

if __name__=='__main__':\
    myapp.run(debug=True)
