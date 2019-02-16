from flask import Flask, render_template, request
import json
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('news-site')

def get_outputs(page):
  response = table.get_item(
    Key={'page': page})
  outputs = response['Item']['content']
  return outputs


@app.route("/", methods=['GET'])
def news_create():
  outputs = get_outputs('news')
  return render_template('news.html', outputs=outputs)

@app.route("/supreme_court", methods=['GET'])
def sp_create():
  outputs = get_outputs('supreme_court')
  return render_template('supreme_court.html', outputs=outputs)

@app.route("/congress", methods=['GET'])
def congress_create():
  outputs = get_outputs('congress')
  return render_template('congress.html', outputs=outputs)

@app.route("/about", methods=['GET'])
def about_create():
  return render_template('about.html')

if __name__ == "__main__":
  app.run(debug=True, host='127.0.0.1')
