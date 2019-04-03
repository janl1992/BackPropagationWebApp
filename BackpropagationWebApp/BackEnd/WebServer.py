from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler;
from MultiLayerPerceptron.MultiLayerPerceptron import startNeuralNetwork;
from MultiLayerPerceptron.MultiLayerPerceptron import Example;
import json as js;
# from MultiLayerPerceptron import MultiLayerPerceptron.startNeuralNetwork();
class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        SimpleHTTPRequestHandler.end_headers(self)

class ExampleEncoder(js.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Example):
            return obj.__dict__
        return js.JSONEncoder.default(self, obj)
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/multilayerperceptron':
            # mp.startNeuralNetwork();
            animationarray, animationarrayreference = startNeuralNetwork()
            jsonanimationarray = js.dumps(animationarray, cls=ExampleEncoder)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(jsonanimationarray.encode('utf-8'))
            # self.wfile.close()
            return
            # print(animationarray)
        if self.path == '/getreference':
            animationarray, animationarrayreference = startNeuralNetwork()
            jsonfinalanimationarray = js.dumps(animationarrayreference[0], cls=ExampleEncoder)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(jsonfinalanimationarray.encode('utf-8'))
            # self.wfile.close()
            return


address = ("127.0.0.1", 8080)

server = HTTPServer(address, MyRequestHandler, CORSRequestHandler)
server.serve_forever()