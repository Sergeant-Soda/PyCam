from flask import Flask, render_template, Response, jsonify
import cv2
import socket
from datetime import datetime

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/info')
def info():
    # Get the computer hostname
    hostname = socket.gethostname()
    # Get the IPv4 address
    ip_address = socket.gethostbyname(hostname)
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Return the information as JSON
    return jsonify(hostname=hostname, ip_address=ip_address, datetime=current_datetime)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
