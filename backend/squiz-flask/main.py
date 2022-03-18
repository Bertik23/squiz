from flask import Flask, jsonify

app = Flask("main")

@app.route("/")
def index():
    return "Hello World"


@app.route("/getQuiz")
def api_getQuiz():
    pass

if __name__ == "__main__":
    app.run()
