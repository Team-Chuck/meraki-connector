"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from MerakiConnector import app
import json
from .models.meraki_scan_model import meraki_scan_from_dict


@app.route('/meraki_scan', methods=['POST'])
def meraki_scan():
    data = request.data
    result = meraki_scan_from_dict(json.loads(request.data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


    