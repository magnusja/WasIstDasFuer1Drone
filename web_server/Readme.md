Little web server for doing classification with caffe over a REST interface with json. Code mainly taken from [this](https://github.com/NVIDIA/DIGITS/tree/master/examples/classification) example. Advantage of this web service is that loading of the net is only done when starting up and not evertime a classification is made.

## Usage
```python main.py <path to .caffemodel> <path to deploy.prototxt> <path to labels.txt> <path to mean.binaryproto>```
