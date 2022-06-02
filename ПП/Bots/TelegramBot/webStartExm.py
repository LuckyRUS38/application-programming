import random

from flask import Flask, render_template

app = Flask(__name__)

images = [
    "https://c.tenor.com/H_4b2t0zoaAAAAAd/python-code.gif",
    "https://c.tenor.com/lpw4aP4SDtAAAAAd/snakes-animal.gif",
    "https://c.tenor.com/_7r8RXryt3QAAAAC/python-powered.gif",
    "https://tenor.com/view/python-gif-20799882",
    "https://c.tenor.com/Zf4eCnr0AvEAAAAd/yawn-snake.gif",
    "https://c.tenor.com/nTLXZxk4CgMAAAAC/snake-hisss.gif"
]


@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
