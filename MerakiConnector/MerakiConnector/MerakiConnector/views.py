"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session
from MerakiConnector import app
import json
from .models.meraki_scan_model import meraki_scan_from_dict, meraki_scan_to_dict
from .models.meraki_scan_v3_model import meraki_scanv3_from_dict, meraki_scanv3_to_dict
from chuck_core import se_handler


@app.route('/meraki_scan', methods=['POST'])
def meraki_scan():
    data = request.data
    valid_macs = ['3c:28:6d:e0:a7:c7', '98:10:e8:12:51:cc', 'a0:c9:a0:f9:43:17', '54:33:cb:ef:cc:13', '88:66:a5:96:7b:82', '3c:28:6d:e0:a7:c6', '54:33:cb:ef:cc:14']
    result = meraki_scan_from_dict(json.loads(request.data))
    if result.type == 'DevicesSeen':
        filtered_list = [x.to_dict() for x in result.data.observations if x.client_mac in valid_macs]
        with open (".\current_locations.json", "w+") as wf:
            wf.write(json.dumps(filtered_list))        
        print("Current locations set to: " + str(filtered_list))
    print(result.type)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/meraki_scan_v3', methods=['POST'])
def meraki_scan_v3():
    data = request.data
    valid_macs = ['3c:28:6d:e0:a7:c7', '98:10:e8:12:51:cc', 'a0:c9:a0:f9:43:17', '54:33:cb:ef:cc:13', '88:66:a5:96:7b:82', '3c:28:6d:e0:a7:c6', '54:33:cb:ef:cc:14', '88:b2:91:40:65:9a']
    result = meraki_scanv3_from_dict(json.loads(request.data))
    if result.type == 'WiFi':
        filtered_list = [x.to_dict() for x in result.data.observations if x.client_mac in valid_macs]
        #with open (".\current_locations.json", "w+") as wf:
        #    wf.write(json.dumps(filtered_list))    
        #with open (".\all_locations.json", "w+") as wf:
        #    wf.write(json.dumps(result))     
        print("Current locations set to: " + str(filtered_list))
    print(result.type)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/meraki', methods=['GET'])
def meraki_polling():
    with open (".\current_locations.json", "r") as rf:
        list = json.load(rf)
    return json.dumps(list), 200, {'ContentType':'application/json'}  


@app.route('/rooms', methods=['GET'])
def room_polling():
    # There is no hard-coding here.. I swear...  
    current_values = se_handler.aggregated_room_data()

    rooms = []
    room_a = [x for x in current_values if 'Conference Room A' in x['id']]
    room_b = [x for x in current_values if 'Conference Room B' in x['id']]
    room_c = [x for x in current_values if 'Conference Room C' in x['id']]
    room_d = [x for x in current_values if 'Conference Room D' in x['id']]

    rooms.append(build_room_data('Conference Room A', room_a))
    rooms.append(build_room_data('Conference Room B', room_b))
    rooms.append(build_room_data('Conference Room C', room_c))
    rooms.append(build_room_data('Conference Room D', room_d))

    return json.dumps(rooms), 200, {'ContentType':'application/json'} 


def build_room_data(name, room_point_values):
    temp = [x for x in room_point_values if x['id'].endswith('/Temp')][0]
    shades = [x for x in room_point_values if x['id'].endswith('/Shade')][0]
    light = [x for x in room_point_values if x['id'].endswith('/Light Status')][0]
    occupied = [x for x in room_point_values if x['id'].endswith('/RoomStatus')][0]
    projector = [x for x in room_point_values if x['id'].endswith('/Projector')][0]

    return { 'name': name,
            'light' : light.get('value'),
             'temp': temp.get('value'),
             'projector': projector.get('value'),
             'occupied' : occupied.get('value'),
             'shades' : shades.get('value'),
             'id' : temp.get('id')[:-12]
            }