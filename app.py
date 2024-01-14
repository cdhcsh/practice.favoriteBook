from flask import Flask,render_template,jsonify,request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

app = Flask(__name__)
client = MongoClient('mongodb+srv://sparta:jungle@cluster0.jxnelzd.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.books

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/books/list",methods=['GET'])
def getBooks():
    books = list(db.book.find({},{'_id':0}).sort('like',-1))
    return jsonify({'result' : 'success','books':books})

@app.route("/api/books/like",methods=['POST'])
def likeBook():
    no = request.form['no_give']
    db.book.update_one({'no':no},{'$inc' : {'like' : 1}})
    like = db.book.find_one({'no':no},{'like':1,'_id':0})['like']
    return jsonify({'result' : 'success','like' : like})

@app.route("/api/books/delete",methods=['POST'])
def deleteBook():
    db.book.delete_one({'no':request.form['no_give']})
    return jsonify({'result' : 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)