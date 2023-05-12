from flask import Flask, make_response

app = Flask(__name__

@app.route('/')
def render_markdown():
    return "## Heading", 200, {'Content-Type': 'text/markdown'}

@app.route('/error404')
def http_404_handler():
    return make_response("404 Error", 400)

@app.route('/error500')
def http_500_handler():
     return"500 Error", 500

@app.route('/books/<genre>/')
def books(genre):
    res = make_response("All Books in {} category".format(genre))
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'Foobar'
    return res

@app.route('/set-cookie')
def set_cookie():
    res = make_response("Cookie setter")
    res.set_cookie("favorite-color", "skyblue", 60*60*24*15)
    res.set_cookie("favorite-font", "sans-serif", 60*60*24*15)
    return res

@app.route('/transfer')
def transfer():
    return "", 302, {'location': 'https://localhost:5000/login'}

if __name__ == '__main__':
    app.run(debug=True)