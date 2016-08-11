import os

import time

import sys
from flask import Flask, jsonify
from flask import request

from web_server.example import get_net, get_transformer, load_image, forward_pass, read_labels

app = Flask(__name__)

# Load the model and images
net = get_net(sys.argv[1], sys.argv[2], True)
transformer = get_transformer(sys.argv[2], None)
_, channels, height, width = transformer.inputs['data']
if channels == 3:
    mode = 'RGB'
elif channels == 1:
    mode = 'L'
else:
    raise ValueError('Invalid number for channels: %s' % channels)

labels = read_labels(sys.argv[3])


@app.route('/classify', methods=['GET', 'POST'])
def classify():

    print request.files

    file_storage = request.files['image_file']
    image = load_image(file_storage, height, width, mode)

    # Classify the image
    scores = forward_pass([image], net, transformer)

    ### Process the results

    indices = (-scores).argsort()[:, :5]  # take top 5 results
    classifications = []
    for image_index, index_list in enumerate(indices):
        result = []
        for i in index_list:
            # 'i' is a category in labels and also an index into scores
            if labels is None:
                label = 'Class #%s' % i
            else:
                label = labels[i]
            result.append((label, round(100.0 * scores[image_index, i], 4)))
        classifications.append(result)

    for index, classification in enumerate(classifications):
        print '{:-^80}'.format(' Prediction for %s ' % [image][index])
        for label, confidence in classification:
            print '{:9.4%} - "{}"'.format(confidence / 100.0, label)
        print

        return jsonify(prediction=classification)

    return 'ok'


@app.route('/hello')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True)