from globals import WAIT, socketio, SPEED, DELTA_TIME, PATH_X, PATH_Y, step, get_distance, x, y, reformat_data
import time

class WebsocketController():
    buffer = {"uav1": [], "uav2": []}
    @staticmethod
    def emit(data, channel="data"):
        socketio.emit(channel, data)
        print("emitted", data)
        time.sleep(WAIT)
    
    @staticmethod
    def push_to_buffer(data, channel="data"):
        if not isinstance(WebsocketController.buffer[data["device"]], list): 
            WebsocketController.buffer[data["device"]] = [data]
        else:
            WebsocketController.buffer[data["device"]].append(data)

        if WebsocketController.buffer["uav1"].__len__() != 0 and WebsocketController.buffer["uav2"].__len__() != 0:
            x, y = next_location()
            car_data = {"device": "car", "long": str(y), "lat": str(x)}
            WebsocketController.emit(
                [
                    reformat_data(WebsocketController.buffer["uav1"][0]),
                    reformat_data(WebsocketController.buffer["uav2"][0]), 
                    reformat_data(car_data)
                ])

            WebsocketController.buffer = {"uav1": [], "uav2": []}


    






def next_location():
    global step
    
    distance = SPEED * DELTA_TIME
    points_distance = get_distance(PATH_X[step], x, PATH_Y[step], y)
    
    x_diff = PATH_X[step] - x
    y_diff = PATH_Y[step] - y
    
    x0 = x + (distance/points_distance)*(x_diff)
    y0 = y + (distance/points_distance)*(y_diff)
    
    x_diff_updated = PATH_X[step] - x
    y_diff_updated = PATH_Y[step] - y
    
    if(x_diff * x_diff_updated < 0 or y_diff * y_diff_updated < 0):
        x0 = PATH_X[step]
        y0 = PATH_Y[step]
        step = (step+1)%len(PATH_X)
    

    return (x0, y0)
