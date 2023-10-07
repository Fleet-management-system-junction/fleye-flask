from mqtt import client
from globals import  uav_data, app, socketio



@app.route('/')
def hello_world():
    return {"message": "Server up"}

@app.route('/uav/<int:id>', methods=["GET"])
def uav_info(id):
    return {"data": uav_data.get(id)}


@socketio.on("connect")
def handle_connect():
    print("client connected");


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('data')
def handle_message(message):
    print('Received message:', message)
    client.loop_read()


if __name__ == '__main__':
    socketio.run(app, debug=True)