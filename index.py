from flask import Flask, render_template, request
import news

app = Flask(__name__)


@app.route("/", methods=['GET'])
def pagecreate():
  outputs = {}
  outputs = news.run(outputs)
  return render_template('index.html', outputs=outputs)

if __name__ == "__main__":
  app.run(debug=True, host='127.0.0.1')
