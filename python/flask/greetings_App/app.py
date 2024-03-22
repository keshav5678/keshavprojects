from flask import *
from flask_cors import CORS, cross_origin
import mysql.connector
from os import urandom
import random
import string
import qrcode
import qrcode.image.svg
import argon2

factory = qrcode.image.svg.SvgPathImage

app = Flask(__name__)
cors = CORS(app)
app.secret_key = urandom(64).hex()
ALLOWED_EXTENSIONS = {"gif"}
app.config["UPLOAD_FOLDER"] = r"static\gifs"

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def allowed_file(filename):
    "this is not required please remove this function"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

database = mysql.connector.connect(
  host="localhost",
  user="root",
  password="YOUR PASSWORD",
  database="greeting_website"
) # change this to your mysql db
cursor = database.cursor()

@app.route("/happyNewYear")
def happy_new_year():
    name = request.args.get("name", default="user")
    title = "happy new year!"
    content = f"wish you a happy new year, {name}"
    return render_template('new_year_greeting.html', title=title, greet_content=content)

@app.route("/")
@cross_origin()
def main():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
@cross_origin()
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = argon2.hash_password(bytes(request.form.get('password'), 'utf-8'))

        cursor.execute("SELECT id FROM users WHERE name=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        if result:
            session["user"] = result[0]
        else:
            return 'incorrect username or password'

        return redirect(url_for('main'))
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
@cross_origin()
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        password = argon2.hash_password(bytes(request.form.get('password'), 'utf-8'))
        id = urandom(12).hex()
        
        cursor.execute("INSERT INTO users (id, name, password) VALUES (%s, %s, %s)", (id, username, password))
        database.commit()
        session['user'] = id

        return redirect(url_for('main'))
    else:
        return render_template("sign_up.html")

@app.route("/editor", methods=["GET", "POST"])
@cross_origin()
def editor():
    if 'user' in session:
        theme_name = request.args.get("theme_name")
        if request.method == "GET":
            return render_template("editor.html", theme_name=theme_name)
        else:
            if theme_name in ["new_year_greeting"]:
                title = request.form.get("title")
                content = request.form.get("content")

                cursor.execute("INSERT INTO greetings (theme, title, content, filename) VALUES (%s,%s,%s,%s)", (theme_name, title, content, "None"))
                database.commit()
            elif theme_name == "blank":
                title = request.form.get("title")
                content = request.form.get("content")
                
                gif_src = request.form.get("gif_src")

                print(theme_name, title, content, gif_src)
                
                cursor.execute("INSERT INTO greetings (theme, title, content, filename) VALUES (%s,%s,%s,%s)", (theme_name, title, content, gif_src))
                database.commit()
            else:
                return 'no such theme'

            cursor.execute("SELECT * FROM greetings")
            greeting_number = len(cursor.fetchall())

            img = qrcode.make(f'{request.root_url}/greeting/{greeting_number}', image_factory = factory)
            img_str = img.to_string(encoding='unicode')

            return f"""
            greeting created! view at <a href="/greeting/{greeting_number}">/greeting/{greeting_number}</a><br>
            {img_str}
            """
    else:
        return redirect(url_for('login'))    
    

@app.route("/greeting/<number>")
def greeting(number):
    try:
        int(number)
    except:
        return "not valid"
    cursor.execute("SELECT * FROM greetings WHERE id=%s", (number,))
    r = cursor.fetchone()
    if not r:
        abort(404)
    else:
        if r[0] != "blank":
            return render_template(f"{r[0]}.html", title=r[1], greet_content=r[2])
        else:
            the_filename = url_for('static', filename=r[3])
            return render_template("blank.html", title=r[1], greet_content=r[2], filename=the_filename)


@app.route("/logout")
@cross_origin()
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('main'))
    else:
        return redirect(url_for('main'))

@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('static', filename="favicon.ico"))

if __name__ == "__main__":
    app.run() # dont use app.run in production
