from flask import *
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="your password",
  database="url_shortening_service"
) # change it to your mysql db

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def homepage():
    if request.method == "POST":
        # storing url in database
        name_of_the_link = request.form.get("nameoflink")
        url_gotten_from_form = request.form.get("linktoshorten")

        name_of_the_link = name_of_the_link.replace(".", "_")

        if url_gotten_from_form.find("https://") == -1:
            x = ''
            url_gotten_from_form = x.join(['https://', url_gotten_from_form])

        the_query = ("INSERT INTO links (linkname, url) VALUES (%s, %s)")
        the_values = (name_of_the_link, url_gotten_from_form)
        mycursor.execute(the_query, the_values)
        mydb.commit()

        # returning the template index.html from the templates folder
        return render_template("index.html")
    return render_template("index.html")

def get_link_from_database(name_to_use):
    mycursor.execute("SELECT url FROM links WHERE linkname=%s", (name_to_use,))
    link_to_use = mycursor.fetchone()

    if link_to_use:
        return link_to_use[0]  # Unpack the result tuple and return the link
    else:
        return None

@app.route('/<name_to_use>')
def host_shortened_url(name_to_use):
    link_to_use = get_link_from_database(name_to_use)
    if link_to_use is not None:
        return render_template("redirect_page.html", url_to_redirect=link_to_use)
    else:
        return "Shortened URL not found."

if __name__ == '__main__':
    app.run()
