from flask import Flask, render_template, request
import scrape

app = Flask(__name__)


@app.route("/", methods=['GET'])
def news_create():
  outputs = {}
  outputs = scrape.news_run(outputs)
  return render_template('news.html', outputs=outputs)

@app.route("/supreme_court", methods=['GET'])
def sp_create():
  outputs = {}
  outputs = scrape.supreme_court_run(outputs)
  return render_template('supreme_court.html', outputs=outputs)

@app.route("/congress", methods=['GET'])
def congress_create():
  outputs = []
  outputs = scrape.congress_run(outputs)
  return render_template('congress.html', outputs=outputs)

@app.route("/about", methods=['GET'])
def about_create():
  outputs = {}
  outputs = scrape.news_run(outputs)
  return render_template('news.html', outputs=outputs)

if __name__ == "__main__":
  app.run(debug=True, host='127.0.0.1')
