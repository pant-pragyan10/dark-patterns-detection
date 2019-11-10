from flask import Flask, jsonify, request
from joblib import load

presence_classifier = load("presence_classifier.joblib")
presence_vect = load("presence_vectorizer.joblib")
category_classifier = load("category_classifier.joblib")
category_vect = load("category_vectorizer.joblib")

app = Flask(__name__)
output = []

@app.route('/', methods=['POST', 'GET'])
def main():
    global output 

    if request.method == 'POST':
        data = request.get_json().get('tokens')

        for token in data:
            result = presence_classifier.predict(presence_vect.transform([token]))
            output.append(result[0])

        dark = [data[i] for i in range(len(output)) if output[i] == 'Dark']
        for d in dark:
            print(d)
        print()
        print(len(dark))
        print(len([out for out in output if out == 'Dark']))
        return 'OK', 200
    elif request.method == 'GET':
        message = '{ "result": ' + str(output) + ' }'
        print(message)

        #print("message: ")
        #print(message)
        json = jsonify(message)
        #print("json: ")
        #print(json)

        output = []

        return json

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
