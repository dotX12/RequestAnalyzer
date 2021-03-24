import re

import flask
from flask import request, jsonify
from six.moves.urllib.parse import urlparse, unquote

sql_xss_pattern = re.compile(
        r'<(|\/|[^\/>][^>]+|\/[^>][^>]+)>|'
        r'(ALTER|CREATE|DELETE|DROP\+|EXEC(UTE){0,1}|'
        r'INSERT( +INTO){0,1}|MERGE\+|\\/\*\*\\/|CONCAT|\)OR\(|\+OR\+|HAVING|--\+|'
        r'TABLE_SCHEMA|SELECT\+|SELECT\(|SELECT\'|UPDATE\+|1=1|1\+=\+1|--|\*/|TRUNCATE|UNION( +ALL){0,1})')

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>DDOS-GUARD</h1>'''


@app.route('/api/v1/exploit', methods=['GET'])
def api_id():
    if 'url' in request.args:
        url = str(request.args['url'])
        upper_text = url.upper()
        decode_url = unquote(upper_text)
        if re.search(sql_xss_pattern, decode_url):
            return jsonify(False)
        else:
            return jsonify(True)
    else:
        return "Error, bad argument."


app.run()