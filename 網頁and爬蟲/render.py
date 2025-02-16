import flask, time

app = flask.Flask(__name__)


@app.route("/")
@app.route("/home")
def home() -> str:
    return flask.render_template("home.html")


@app.route("/web.1")
@app.route("/web/1")
@app.route("/web1")
def web1() -> str:
    return flask.render_template("web1.html")


@app.route("/show.<name>", methods=["GET"])
@app.route("/show/<name>", methods=["GET"])
def show(name: object) -> str:
    return f"<html><body><h1>{name}</h1><h3><a href='http://127.0.0.1:5000'>home</a></h3></body></html>"


@app.route("/time")
def t() -> str:
    while True:
        t = time.localtime()
        return flask.render_template("time.html", ti=f"{t[0]}/{t[1]}/{t[2]} {t[3]}:{t[4]}:{t[5]}")


@app.route("/道德經")
def TaoTeChing() -> str:
    return flask.render_template("道德經.html")


@app.route("/質數.<p>", methods=["GET"])
@app.route("/質數/<p>", methods=["GET"])
def PrimeNumber(p: str) -> str:
    n = int(p)
    if n < 0:
        a = 0
    elif n == 2:
        a = 1
    elif n == 1 or n == 0:
        a = 1
    else:
        for i in range(3, n, 2):
            if n % i == 0:
                a = 2
                break
        else:
            a = 1
    if a == 0:
        a = "輸入錯誤"
    elif a == 1:
        a = f"{n}是質數"
    else:
        a = f"{n}不是質數"
    return f"<html><body><h1>{a}</h1><h3><a href='http://127.0.0.1:5000'>home</a></h3></body></html>"


def f2(b: int) -> bool:
    if b == 2:
        return True
    if b % 2 == 0:
        return False
    for i in range(3, b // 2 + 2, 2):
        if b % i == 0:
            return False
    else:
        return True


@app.route("/質數因數分解.<N>", methods=["GET"])
@app.route("/質數因數分解/<N>", methods=["GET"])
def pn(N: str) -> str:
    try:
        n = int(N)
    except:
        return f"<html><body><h1>錯誤: 輸入須為正整數</h1><h3><a href='http://127.0.0.1:5000'>home</a></h3></body></html>"
    if n <= 0:
        a = "錯誤: 輸入須為正整數"
    if n == 1:
        a = "1"
    i = 2
    f: dict[int, int] = {}
    while n > 1:
        while n % i == 0:
            n = n // i
            if i in f:
                f[i] += 1
            else:
                f[i] = 1
        i += 1
        while not f2(i):
            i += 1
    if len(f) == 1:
        a = N + "是質數"
    else:
        a = N + " = " + " * ".join(str(k) if v == 1 else f"{k}^{v}" for k, v in f.items())
    return f"<html><body><h1>{a}</h1><h3><a href='http://127.0.0.1:5000'>home</a></h3></body></html>"


if __name__ == "__main__":
    app.run()
