from flask import Flask, render_template, request, jsonify
from classifier.main import classify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/classify', methods=['POST'])
def classifier():
    apps = request.get_json()['apps']
    classified_apps = classify(apps)
    r = {"apps": classified_apps}
    return jsonify(r)


if __name__ == '__main__':
    app.run()
