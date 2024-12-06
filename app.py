from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/hello/')
def hello_world():
    my_html = f"<body style='background-color: #6bc930;'><h1 style='color:  #0a0a0a;'>Green Version: V2</h1>"
    return my_html

@app.route('/<username>')
def hello_user(username):
    my_html = f"<body style='background-color: #6bc930;'><h1 style='color:  #0a0a0a;'>Hello {username} you are accessing the Green Version of the app: V2</h1>"
    return my_html

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090)