from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

DEVICE_COUNT = 2
queues = {0: [], 1: []}      # For managing lat, lon from mqtt
uav_data = {}   # For http requests on specific uav data

topics = lambda X: {
    0: f"uav{X}/gps/lat", 
    1: f"uav{X}/gps/lon", 
    2: f"uav{X}/bat/id", 
    3: f"uav{X}/bat/vl", 
    4: f"uav{X}/bat/pt",
    5: f"uav{X}/gps/fx", 
    6: f"uav{X}/gps/fx",
    7: f"uav{X}/gps/ns",
    8: f"uav{X}/gps/abs",
    9: f"uav{X}/gps/rel",
    10: f"uav{X}/in_air",
    11: f"uav{X}/armed",
    12: f"uav{X}/armed",
    13: f"uav{X}/state",
    14: f"uav{X}/mav_msg",
    15: f"uav{X}/health",
    16: f"uav{X}/fm"
}

WAIT = 1
SPEED = .0003

DELTA_TIME = 1

PATH_Y = [36.69096479049644, 36.6901492026491, 36.69011934968361, 36.69036729568651, 36.69087810983597, 36.691335849510324, 36.69126619365008, 36.691541499777145, 36.691654275513116, 36.69181017108798, 36.69189309412059, 36.69163769084219, 36.69148842879321, 36.690964350850805, 36.69045685425646, 36.69019812921278, 36.690218031169344]

PATH_X = [2.8499831679168985, 2.8544248772472534, 2.856141537957721, 2.8576233014933123, 2.8589387186344233, 2.8600473091651235, 2.8603037741439366, 2.8607463830589848, 2.8609159808375373, 2.8609035712417876, 2.8603658221226818, 2.8601134936757844, 2.8599728515906286, 2.85889735331526, 2.857561253514567, 2.8561465596215365, 2.8544588546027447]






# x_path_history = []
# y_path_history = []

def get_distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5


def reformat_data(data):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [data["lat"], data["long"]]
        },
        "properties": {
            "name": data["device"]
        }
    } 