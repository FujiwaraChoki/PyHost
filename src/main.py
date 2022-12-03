# PyHost

from http.server import BaseHTTPRequestHandler, HTTPServer


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


routes = []


class PyHost():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            print("Current path: " + self.path)
            # Handle GET requests, using objects in routes
            for obj in routes:
                if self.path == obj["route"] and str(obj["method"]).lower() == "get":
                    self.send_response(200)
                    # Send headers
                    for key, value in obj["response_headers"].items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(
                        bytes(obj["response"], "utf8"))
                    return

            self.send_response(404)

        def do_POST(self):
            for obj in routes:
                if self.path == obj["route"] and str(obj["method"]).lower() == "post":
                    self.send_response(200)
                    # Send headers
                    self.end_headers()
                    # Send custom reply
                    self.wfile.write(
                        bytes(obj.handler(), "utf8"))

                    return

    def warn(self, message):
        print(bcolors.WARNING + "WARNING:\t" + message + bcolors.ENDC)

    def error(self, message):
        print(bcolors.FAIL + "ERROR:\t" + message + bcolors.ENDC)

    def success(self, message):
        print(bcolors.OKGREEN + "SUCCESS:\t" + message + bcolors.ENDC)

    def msg(self, message):
        print("MSG:\t" + message)

    def get(self, route, response="<h1>Default Response</h1>", response_headers={"Content-type": "text/html"}):
        # Add route to routes
        routes.append({
            "method": "GET",
            "route": route,
            # The HTML response
            "response": response,
            "response_headers": response_headers
        })

    def post(self, route, response_headers, handler):
        # Handle POST requests, using objects in routes
        routes.append({
            "method": "POST",
            "route": route,
            "response": response_headers,
            # Handler is a function that handles the POST request
            "handler": handler
        })

    def serve(self):
        # Start server
        server = HTTPServer((self.host, self.port), PyHost.Handler)
        self.success("Server started http://%s:%s" %
                     (self.host, self.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            self.warn("Stopping server...")
            self.success("Server stopped")
        server.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    server = PyHost("localhost", 8080)
    server.get(route="/", response_headers={"Content-type": "text/html"},
               response=open("index.html", "r").read())
    server.get(route="/test", response_headers={"Content-type": "text/html"},
               response=open("test.html", "r").read())
    server.serve()