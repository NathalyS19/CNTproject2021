from flask import Flask, render_template, request, flash, Response
import os
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)
app.secret_key = os.urandom(24)

def generate():
    while True:
        success,frame = camera.read()
        if not success:
            break
        else:
            ret,buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/staticfeed')
def staticfeed():
    return render_template('staticfeed.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    if password == 'Testing123' and username == 'admin':
        return render_template('homepage.html')
    else:
        flash('Wrong username or password!')
        return render_template('login.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
