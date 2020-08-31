
import flask
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from flask import request, jsonify


executor = ThreadPoolExecutor(100)
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')



@app.route('/qycx', methods=['get'])
def xwcks():
    try:
        book = {'a':'123'}
        return jsonify({'code': 200, 'message': book})
    except Exception as e:
        print(e)
        return jsonify({'code': 404, 'message': '接口出错'})


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)
