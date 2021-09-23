import re
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


ENV = 'int'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/todo'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zmawqelhmwsuku:e745a32366e04cbe3021e13ee8e9e84ddaae6e8bb60df49b71963428986e5955@ec2-34-197-135-44.compute-1.amazonaws.com:5432/dc4obd2ivb35ll'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class yapilacaklar(db.Model):
    __tablename__ = 'yapilacaklar'
    id = db.Column(db.Integer, primary_key = True)
    yapilacak = db.Column(db.String(200))

    def __init__ (self,yapilacak):
        self.yapilacak = yapilacak

class tamamlananlar(db.Model):
    __tablename__ = 'tamamlananlar'
    id = db.Column(db.Integer, primary_key = True)
    tamamlanan = db.Column(db.String(200))

    def __init__ (self,tamamlanan):
        self.tamamlanan = tamamlanan

@app.route('/')
def index():
    yapilacaklar_listesi = yapilacaklar.query.all()
    tamamlananlar_listesi = tamamlananlar.query.all()
    return render_template('index_yapilacaklar.html',yapilacaklar_listesi = yapilacaklar_listesi,tamamlananlar_listesi = tamamlananlar_listesi)

@app.route('/tamamlananlarListesi')
def tamamlananlarListesi():
    yapilacaklar_listesi = yapilacaklar.query.all()
    tamamlananlar_listesi = tamamlananlar.query.all()
    return render_template('index_tamamlananlar.html',yapilacaklar_listesi = yapilacaklar_listesi,tamamlananlar_listesi = tamamlananlar_listesi)

@app.route('/ekle', methods = ['POST'])
def ekle():
    if(request.method == 'POST'):
        yeni_yapilacak = request.form['yeni_yapilacak']
        if(yeni_yapilacak != ''):
            data = yapilacaklar(yeni_yapilacak)
            db.session.add(data)
            db.session.commit()
    return redirect(url_for("index"))

@app.route('/tamamla/<string:id>', methods = ['POST'])
def tamamla(id):
    data = yapilacaklar.query.filter_by(id=id).first()
    data_icerik = data.yapilacak
    db.session.delete(data)
    data_tamamlanmis = tamamlananlar(data_icerik)
    db.session.add(data_tamamlanmis)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/tamamlanmamisIsaretle/<string:id>', methods = ['POST'])
def tamamlanmamisIsaretle(id):
    data = tamamlananlar.query.filter_by(id=id).first()
    data_icerik = data.tamamlanan
    db.session.delete(data)
    data_yapilacak = yapilacaklar(data_icerik)
    db.session.add(data_yapilacak)
    db.session.commit()
    return redirect(url_for("tamamlananlarListesi"))

@app.route('/yapilacakSil/<string:id>', methods = ['POST'])
def yapilacakSil(id):
    data = yapilacaklar.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/tamamlanmisSil/<string:id>', methods = ['POST'])
def tamamlanmisSil(id):
    data = tamamlananlar.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("tamamlananlarListesi"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()