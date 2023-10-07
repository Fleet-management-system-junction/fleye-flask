from globals import topics, uav_data, queues, socketio
from controllers.websocket_controller import WebsocketController

class MQTTController():

    @staticmethod
    def on_message(client, userdata, msg):
        data = msg.payload.decode()
        for i in [1, 2]:
            if (msg.topic == topics(i)[0]):
               MQTTController.handle_topic_0(uav_id=i, queue=queues[ i - 1], data=data, socketio=socketio)
            elif (msg.topic == topics(i)[1]):
                MQTTController.handle_topic_1(uav_id=i, queue=queues[i - 1], data=data, socketio=socketio)
            else: 
                MQTTController.handle_uav_data(uav_id=i, topic=msg.topic, uav_data=uav_data, data=data)
            


    @staticmethod
    def on_connect(client, userdata, flags, rc):
        for i in [1, 2]: #uav 1, uav 2
            for pos, topic in topics(i).items():
                client.subscribe(topic, 2)
                print(f"connected to {topic}")


    @staticmethod
    def handle_topic_0(uav_id, queue, data, socketio):
        if (queue.__len__() == 0):
            queue.append((data, None))
        elif  queue[-1][0] == None:
            queue[-1] = (data, queue[-1][1]) 
            WebsocketController.push_to_buffer({"device": f"uav{uav_id}" ,"long": queue[-1][0], "lat": queue[-1][1]})
            queue.pop(-1)

    @staticmethod
    def handle_topic_1(uav_id, queue, data, socketio):
        if (queue.__len__() == 0):
            queue.append((None, data))
        elif  queue[-1][1] == None:
            queue[-1] = (queue[-1][0], data) 
            WebsocketController.push_to_buffer({"device": f"uav{uav_id}", "long": queue[-1][0], "lat": queue[-1][1]})
            queue.pop(-1)
   
    @staticmethod
    def handle_uav_data(uav_id, topic, uav_data, data):
        if isinstance(uav_data.get(uav_id), dict):
            uav_data[uav_id][topic] = data
        else:
            uav_data[uav_id] = {topic: data}        