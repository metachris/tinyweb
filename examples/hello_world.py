#!/usr/bin/env micropython
"""
Test the server routes:

$ curl -vvvv http://localhost:8081
$ curl -vvvv http://localhost:8081/table
$ curl -vvvv http://localhost:8081/redirect
"""
import tinyweb

app = tinyweb.webserver()


# Index page
@app.route('/')
async def index(request, response):
    # Send HTML page with content-type text/html
    await response.html('<html><body><h1>Hello, world! (<a href="/table">table</a>)</h1></html>\n')


# Catch all requests with an invalid URL
@app.catchall()
async def catchall_handler(request, response):
    response.code = 404
    await response.html('<html><body><h1>My custom 404</h1></html>\n')


# HTTP redirection
@app.route('/redirect')
async def redirect(request, response):
    await response.redirect('/')


# Another one, more complicated page
@app.route('/table')
async def table(request, response):
    # Start HTTP response with content-type text/html
    await response.html('<html><body><h1>Simple table</h1>'
                        '<table border=1 width=400>'
                        '<tr><td>Name</td><td>Some Value</td></tr>')
    for i in range(10):
        await response.send('<tr><td>Name{}</td><td>Value{}</td></tr>'.format(i, i))
    await response.send('</table>'
                        '</html>')


def run():
    app.run(host='0.0.0.0', port=8081)


if __name__ == '__main__':
    run()
