from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/classify', methods=['POST'])
def classify():
    apps = request.get_json()['apps']
    classified_apps = classify_apps(apps)
    r = {
        "apps": classified_apps}
    return jsonify(r)


def classify_apps(apps):
    return [
        {
            "name": apps[0],
            "genre": "some genre",
            "artwork": "https://lh3.googleusercontent.com/ESIjDJWm7riHO32Jn9m9408CK8_Pq9-dvNObqNprF8BnTuwlBjCRxtM4Vr-Scqmvwd4=w300"
        },
        {
            "name": apps[1],
            "genre": "some genre",
            "artwork": "https://lh3.googleusercontent.com/ESIjDJWm7riHO32Jn9m9408CK8_Pq9-dvNObqNprF8BnTuwlBjCRxtM4Vr-Scqmvwd4=w300"
        },
        {
            "name": apps[2],
            "genre": "some genre",
            "artwork": "https://lh3.googleusercontent.com/ESIjDJWm7riHO32Jn9m9408CK8_Pq9-dvNObqNprF8BnTuwlBjCRxtM4Vr-Scqmvwd4=w300"
        }
    ]


if __name__ == '__main__':
    app.run()
