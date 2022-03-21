from flask import Flask, jsonify, request, abort
from database import connection
from random import sample, choice, randint
from time import time

app = Flask("main")

@app.after_request
def api_after(f):
    f.headers.add('Access-Control-Allow-Origin', '*')
    return f

SWAPABLE = [
    ("W", "V"),
    ("B", "P"),
    ("M", "N")
]


def isNumber(num: str):
    try:
        int(num)
        return True
    except ValueError:
        return False


def time_micro():
    return int(time()*1000)


def makeQuiz(x, y, a, b):
    differentIndex = 0
    placedDifferent = False


    quizStr = ""
    quizList = []
    for i in range(x):
        quizList.append([])
        quizStr += "\n"
        for j in range(y):
            if not placedDifferent and randint(1, x*y) == 1:
                quizStr += b
                quizList[i].append(b)
                differentIndex = i * x + j
                placedDifferent = True
                continue
            
            quizStr += a
            quizList[i].append(a)
    quizStr = quizStr.strip()
    if not placedDifferent:
        differentIndex, quizStr, quizList = makeQuiz(x, y, a, b)
    return differentIndex, quizStr, quizList


@app.route("/")
def index():
    return "Hello World"


@app.route("/getQuiz")
def api_getQuiz():
    x = request.args.get("x", 10)
    y = request.args.get("y", 10)
    a, b = sample(choice(SWAPABLE), 2)
    print(a, b)

    differentIndex, quizStr, quizList = makeQuiz(x, y, a, b)

    gameId = time_micro()
    with connection() as cur:
        cur.execute(
            "INSERT INTO games (game, correct, id) VALUES (?, ?, ?)",
            (quizStr, differentIndex, gameId)
        )

    return jsonify({
        "id": gameId,
        "game": quizList,
        "game_str": quizStr
    })


@app.route("/submitQuiz")
def api_submitQuiz():
    submitTime = time_micro()
    username: str = request.args.get("username", None)
    gameId: str = request.args.get("id", None)
    differentIndex: str = request.args.get("differentIndex", None)

    if (
        gameId is None
        or
        differentIndex is None
        or
        not isNumber(differentIndex)
        or
        not isNumber(gameId)
    ):
        abort(400)

    gameId = int(gameId)
    timeTook = min(submitTime - gameId, 7000)

    with connection() as cur:
        cur.execute(
            "SELECT correct FROM games WHERE id = ? AND result IS NULL",
            (gameId,)
        )
        game = cur.fetchone()
        won = differentIndex == str(game[0]) and timeTook <= 7000
        if not won:
            timeTook = 7000
        cur.execute(
            "UPDATE games SET inputed = ?, username = ?, time = ?, result = ?"
            "WHERE id = ?",
            (differentIndex, username, timeTook, int(won), gameId)
        )
    return jsonify({
        "correct": won
    })

@app.route("/getUser/<user>")
def api_getUser(user: str):
    with connection() as cur:
        cur.execute(
            "SELECT result, time FROM games WHERE username = ?",
            (user, )
        )

        playerRecords = cur.fetchall()
    playerAvgTime = sum(r[1] for r in playerRecords)/len(playerRecords) if playerRecords else 0
    playerSuccessRate = sum(r[0] for r in playerRecords)/len(playerRecords) if playerRecords else 0

    return jsonify({
        "average_time": playerAvgTime,
        "success_rate": playerSuccessRate,
        "raw_data": playerRecords,
    })




if __name__ == "__main__":
    app.run(debug=True)
