from globals import WAIT, socketio, SPEED, DELTA_TIME, PATH_X, PATH_Y, get_distance, reformat_data
import time

class WebsocketController():
    car_dict = {'x': PATH_X[0], 'y': PATH_Y[0], 'step': 1}
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
            x, y, step = next_location(WebsocketController.car_dict['x'], WebsocketController.car_dict['y'], WebsocketController.car_dict['step'])
            WebsocketController.car_dict['x'] = x
            WebsocketController.car_dict['y'] = y
            WebsocketController.car_dict['step'] = step
            print("outside", WebsocketController.car_dict)
            car_data = {"device": "car", "long": str(WebsocketController.car_dict['y']), "lat": str(WebsocketController.car_dict['x'])}
            WebsocketController.emit(
                [
                    reformat_data(WebsocketController.buffer["uav1"][0]),
                    reformat_data(WebsocketController.buffer["uav2"][0]), 
                    reformat_data(car_data)
                ])

            WebsocketController.buffer = {"uav1": [], "uav2": []}


    






def next_location(x, y, step):

    print("before", x, y)
    distance = SPEED * DELTA_TIME
    points_distance = get_distance(PATH_X[step], x, PATH_Y[step], y)
    
    x_diff = PATH_X[step] - x
    y_diff = PATH_Y[step] - y
    
    x = x + (distance/points_distance)*(x_diff)
    y = y + (distance/points_distance)*(y_diff)
    
    x_diff_updated = PATH_X[step] - x
    y_diff_updated = PATH_Y[step] - y
    
    if(x_diff * x_diff_updated < 0 or y_diff * y_diff_updated < 0):
        x = PATH_X[step]
        y = PATH_Y[step]
        step = (step+1)%len(PATH_X)
    

    print("after", x, y)
    return (x, y, step)

