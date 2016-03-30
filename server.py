from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/start-testing", methods=['POST'])
def start_testing():
    rootUrl = request.form['rootUrl']
    numberOfConcurrentUsers = request.form['numberOfConcurrentUsers']
    numberOfJobsPerUser = request.form['numberOfJobsPerUser']


if __name__ == "__main__":
    app.run(debug=True)
