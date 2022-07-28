# import main Flask class and request object
from flask import Flask, request

# create the Flask app
app = Flask(__name__)


@app.route('/weather')
def query_example():
    params = request.args
    temperature = None
    device_id = None
    humidity = None
    try:
        temperature = params['temp']
    except Exception:
        print('ups')
    try:
        humidity = params['humid']
    except Exception:
        print('ups')
    try:
        device_id = params['id']
    except Exception:
        print('ups')
    to_print = "Device: %s\nTemperature: %s\nHumidity: %s\n=========\n\n" % (device_id, temperature, humidity)
    print(to_print)
    return to_print


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')