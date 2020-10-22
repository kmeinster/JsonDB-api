from flask import Flask, request, jsonify
from libs.query import search_all_objects_within_time_range

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/query', methods=['POST'])
def query():
    content = request.json
    # if content['rangeRaw']:
    #     print('Has rangeRaw')
    if content['range']:
        print(search_all_objects_within_time_range(metric='humidity',
                                                   start_time=content['range']['from'],
                                                   end_time=content['range']['to']))
    # print(content['range'])
    return 'This was a POST'

if __name__ == '__main__':
    app.run()
