from flask import Flask, request, abort, send_from_directory
import os
import hashlib
from werkzeug.utils import secure_filename
from models import db, File, User
from auth import login_required

app = Flask(__name__)
# set the maximum file size at 100 Mb
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db.init_app(app)
with app.app_context():
    db.create_all()
    # create 2 users for test purposes
    if not User.query.filter_by(username='user1').first():
        new_user = User(username='user1', password='1234')
        db.session.add(new_user)
        db.session.commit()
    if not User.query.filter_by(username='user3').first():
        new_user = User(username='user3', password='1234')
        db.session.add(new_user)
        db.session.commit()


def save_path(one_file):
    cwd = os.getcwd()
    hsh = hashlib.sha256(one_file.read()).hexdigest()
    one_file.seek(0) # put file decriptor to begin position
    path = os.path.join(cwd, 'store', hsh[0:2])
    os.makedirs(path, exist_ok = True)
    joined_path = os.path.join(path, hsh)
    return joined_path, hsh


def file_delete(hsh):
    cwd = os.getcwd()
    path = os.path.join(cwd, 'store', hsh[0:2], hsh)
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False


@app.route("/api/", methods=['GET'])
def download():
    hsh = request.form['data']
    cwd = os.getcwd()
    uploads = os.path.join(cwd, 'store', hsh[0:2], hsh)
    if os.path.exists(uploads):
        return send_from_directory(os.path.dirname(uploads), os.path.basename(uploads)), 200
    else:
        return "File not found", 404


@app.route("/api/", methods=['DELETE'])
@login_required
def delete():
    hsh = request.form['data']
    #print(hsh)
    user = User.query.filter_by(username=request.authorization.username).first()
    one_file = File.query.filter_by(hash=hsh, user_id=user.id).first()

    if not one_file:
        return "File not found or acesss denied", 404
    
    if file_delete(hsh):
        db.session.delete(one_file)
        db.session.commit()
        return "Deleted", 200
    else:
        return "File not found", 400
    

@app.route('/api/', methods=['POST'])
@login_required
def upload():
    '''file upload, basic auth'''
    if not request.files:
            abort(400, 'No downloaded file')
    one_file = request.files['file']
    if secure_filename(one_file.filename) == '':
            abort(400, 'Empty file name, file not selected')

    if one_file:
        path, hsh = save_path(one_file)
        #TODO тут добавить try catch конструкцию
        try:
            one_file.save(path)
        except:
            return "Unable to save a file", 400
        username = request.authorization.username
        user = User.query.filter_by(username=username).first()
        new_file = File(hash=hsh, user_id=user.id)
        db.session.add(new_file)
        db.session.commit()
        one_file.close()
        return hsh, 201
    else:
        return "None file", 400

if __name__ == "__main__":
    app.run()
