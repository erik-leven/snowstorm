from flask import Flask, request, Response
import logging
import requests
import os 
import json

app = Flask(__name__)

logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('snowstorm')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

@app.route("/<path>", methods=["POST", "GET"])
def post(path):
    entities = request.get_json()
    return_entities = []
    for entity in entities:
        url_string = entity["ecl"]
        map_target = entity["legemiddel_maptarget"]
        url = os.environ.get("url") + "/" + path + "?etc=" + url_string
        response = requests.get(url, data=json.dumps(entity), headers={"Accept": "application/json","Accept-Language": "no-X-61000202103,en-X-900000000000509007"})
        if response.status_code != 200:
            raise AssertionError ("Unexpected response for entity id %s with status code: %d with response text %s"%(entity["_id"], response.status_code, response.text))
        else:
            logger.info("Successfully sent entity id %s with status code 200" % entity["_id"])
        result_entity = json.loads(response.content.decode())
        result_entity["legemiddel_maptarget"] = map_target
        result_entity["_id"] = entity["_id"]
        return_entities.append(result_entity)
        logger.info("Successfully sent entity id %s with status code 200" % entity["_id"])

    return Response(json.dumps(return_entities), mimetype="application/json")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))