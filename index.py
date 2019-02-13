from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def pagecreate():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True, host='127.0.0.1')
