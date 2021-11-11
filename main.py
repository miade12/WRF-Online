#import flask
#from flask import *
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/addition', methods=['POST'])
def createImage():
    data = request.json
    result = data["num1"] + data["num2"]
    return jsonify({"result": result})


app.run(port=3000)
