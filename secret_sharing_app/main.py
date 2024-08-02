from flask import Flask, render_template, request
from secret_sharing_app.lib import lagrange_interpolation, PolynomialModulo
from random import randint

app = Flask(__name__)

M = 1000000007

@app.route("/")
def welcome():
    return render_template('welcome.html', modulus=M)

def create_polynomial(
        secret: int, degree: int) -> PolynomialModulo:
    """Creates a random polynomial of degree n with the constant term equal to
    `secret`."""
    coeffs = [secret] + [
        randint(0, M - 1)
        for _ in range(1, degree)
    ]
    return PolynomialModulo(coeffs, M)

@app.route("/generate", methods=['POST'])
def generate():
    secret = int(request.form['secret'])
    num_parts = int(request.form['num_parts'])
    degree = int(request.form['degree'])

    poly = create_polynomial(secret, degree)

    parts = [
        (i, poly.eval(i))
        for i in range(1, num_parts + 1)
    ]

    return render_template('generate.html', parts=parts, degree=degree)

@app.route("/restore", methods=['POST'])
def restore():
    degree = int(request.form['degree'])
    return render_template('restore.html', degree=degree)

@app.route("/final", methods=['POST'])
def final():
    print(request.form)
    degree = int(request.form['degree'])
    points = []
    for i in range(degree):
        x_i = int(request.form['x_%d' % i])
        y_i = int(request.form['y_%d' % i])
        points.append((x_i, y_i))
    poly = lagrange_interpolation(points, M)
    return render_template('final.html', secret=poly.eval(0))
    