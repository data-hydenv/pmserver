from glob import glob

from flask import Flask, render_template, jsonify, request, flash
from datetime import datetime as dt

from pmserver.sensor import Sensor
from pmserver import __version__ as version_number

app = Flask(__name__)
app.secret_key = '323rjf42p3rr2j38'

# build a default sensor
pmSensor = Sensor('/dev/ttyUSB0', 9600)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # get the form data
    dev = request.form.get('device')
    baud = request.form.get('baud')
    if dev is None or baud is None:
        flash('No device found', category='danger')
    else:
        pmSensor.port = dev
        pmSensor.baud = baud
        if not pmSensor.connected:
            flash('Device is corrupted', category='danger')

    return render_template('dashboard.html', version=version_number)


@app.route('/', methods=['GET'])
@app.route('/config', methods=['GET'])
def config():
    # get all USB devices. Kind of dirty and Linux specific
    # devices = glob('/dev/ttyUSB*')
    devices = pmSensor.devices()

    # render
    return render_template('config.html', devices=devices)


@app.route('/devices', methods=['GET'])
def devices():
    dev = pmSensor.devices()

    return jsonify({'found': len(dev), 'devices': dev}), 200


@app.route('/status', methods=['GET'])
def status():
    return jsonify(pmSensor.to_dict()), 200


@app.route('/measure', methods=['GET'])
def measure():
    if pmSensor.connected:
        pm10, pm25 = pmSensor.measure()
        tstamp = dt.utcnow()
        return jsonify({
            'time': tstamp,
            'timestamp': tstamp.timestamp(),
            'PM10': pm10,
            'PM25': pm25
        }), 200
    else:
        return jsonify({'message': 'Sensor not found.'}), 404


if __name__=='__main__':
    app.run()