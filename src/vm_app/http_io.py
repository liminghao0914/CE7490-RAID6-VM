import os
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def init():
    return 'Start!'


@app.route('/write', methods=['POST'])
def write():
    data = request.data
    try:
        with open("disk", 'wb+') as f:
            f.write(data)
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        return f'Bad request: {e}', 400


@app.route('/read', methods=['GET', 'POST'])
def read():
    filename = "disk"
    try:
        with open(filename, 'rb') as f:
            data = list(f.read())
            if True:
                app.logger.info(f"read {filename}")
                app.logger.info(data)
                app.logger.info('\n')
            return data, 200
    except Exception as e:
        app.logger.error(e)
        return f'Bad request: {e}', 400

@app.route('/fail', methods=['POST'])
def fail():
    try:
        os.remove("disk")
        return 'OK', 200
    except Exception as e:
        app.logger.error(e)
        return f'Bad request: {e}', 400

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    try:
        is_exist = os.path.exists("disk")
        return str(is_exist), 200
    except Exception as e:
        app.logger.error(e)
        return f'Bad request: {e}', 400


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)