from flask import Flask
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True,host='192.168.0.101', port=8000)