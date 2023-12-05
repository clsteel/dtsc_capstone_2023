from flask import request, Flask
import analysis


app = Flask(__name__)
analysis.initialize_model()


@app.route("/")
def home_page():
    with open('homepage.html', 'r') as f:
        html = f.read()
        return html


@app.route("/project", methods=['GET', 'POST'])
def capstone_page():
    with open('project.html', 'r') as f:
        html = f.read()
        if request.method == "POST":
            # print(request.get_data())
            output = analysis.analyze_form_data(request.form)
            html = html.replace('<!--replaceme-->', '<h2>' + output + '</h2>')
            # last step: insert output into the html we're returning
        return html


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
