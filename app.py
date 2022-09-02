from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://kesesi_bligo_cianjur:kesesi_bligo_cianjur_lx@cluster0.5j4rhuo.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    file = request.files["file_give"]

    # fish.jpg => ['fish', jpg']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    # 2022-09-01-16-40-42
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    # hasil: file-2022-09-01-16-40-42.jpg
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)
    
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_name = f'profile-{mytime}.{extension}'
    save_to = f'static/{profile_name}'
    profile.save(save_to)

    doc = {
        'title':title_receive,
        'content':content_receive,
        'image':filename,
        'profile': profile_name,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)