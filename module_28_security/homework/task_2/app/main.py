from flask import Flask, request, render_template


from flask_cors import cross_origin

ORIGIN = "http://localhost:8080"

app = Flask(__name__, static_folder='./static/')

csp = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    f"connect-src 'self' {ORIGIN}; "
    "img-src 'self' data:; "
    "font-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'; "
    "block-all-mixed-content; "
    "upgrade-insecure-requests;"
)


@app.route('/', methods=['GET'])
@cross_origin(origins=[ORIGIN], methods='GET', headers={'Content-Type'
                                                        'Content-Security-Policy': csp})
def handler():
    print(request.headers)
    user_input = request.args.get('user')
    print(user_input)
    return render_template('hw.html', user_input=user_input)


@app.route('/xss', methods=['GET'])
def handler_xss():
    """http://localhost:8080/xss?user=%3Csvg%20onload=%22alert(%27XSS%27)%22%3E"""
    print(request.headers)
    user_input = request.args.get('user')
    return render_template('hw2.html', user_input=user_input)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
