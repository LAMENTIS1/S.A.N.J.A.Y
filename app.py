from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, async_mode='eventlet')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug('Home route accessed')
    return "Flask server API for the cloud"

@app.route('/give/<message>', methods=['GET'])
def give_message(message):
    # Emit the message to all connected clients
    socketio.emit('broadcast', {'message': message})  
    return f'Message "{message}" sent to all clients!'

@socketio.on('connect')
def handle_connect():
    app.logger.debug('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.debug('Client disconnected')

if __name__ == '__main__':
    app.logger.info("Server is running")
    socketio.run(app)
