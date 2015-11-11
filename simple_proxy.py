import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient

client = tornado.httpclient.AsyncHTTPClient(max_clients=1000)

class Handler(tornado.web.RequestHandler):
    def callback(self, resp):
        try:
            self.write(resp.body)
        finally:
            self.finish()

    @tornado.web.asynchronous
    def get(self, path):

        print("change port: " + path)

        req = tornado.httpclient.HTTPRequest('http://0.0.0.0:9000/' + path)

        client.fetch(req, self.callback)

application = tornado.web.Application([
        (r'/(.*)', Handler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
