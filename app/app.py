from flask import request, Flask
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
print('Loading trained model complete')

@app.route("/")
def home_page():
    with open('homepage.html', 'r') as f:
        html = f.read()
        return html


genres = ['action', 'crime']
@app.route("/project", methods=['GET','POST'])
def capstone_page():
    with open('project.html', 'r') as f:
        html = f.read()
        if request.method == "POST":
            print(request.get_data())
            genres_on = [g for g in genres if g in request.form.keys()]
            runtime = request.form['runtime']
            synopsis = request.form['synopsis']

        return html

    #     user = request.form["nm"]
    #     return redirect(url_for("user", usr=user))
    # else:
    #     return render_template("login.html")

@app.route("/resume")
def resume_page():
    with open('resume.html', 'r') as f:
        html = f.read()
        return html

@app.route("/other-work")
def projects_page():
    with open('other_work.html', 'r') as f:
        html = f.read()
        return html


if __name__ == '__main__':
    app.run(port=80)
