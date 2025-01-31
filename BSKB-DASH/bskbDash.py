import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Initialize the initial values of the toggle buttons
title_status = 0
reverse_status = 0
hBonus_status = 0
vBonus_status = 0
period_status = 0


# Create an initial XML structure
root = ET.Element('info')
title_elem = ET.SubElement(root, 'title')
reverse_elem = ET.SubElement(root, 'reverse')

vBonus_elem = ET.SubElement(root, 'vBonus')
hBonus_elem = ET.SubElement(root, 'hBonus')
period_elem = ET.SubElement(root, 'period')



@app.route('/', methods=['GET', 'POST'])
def index():
    global title_status, reverse_status, vBonus_status, hBonus_status, period_status

    if request.method == 'POST':
    
        if 'title' in request.form:
            title_status = int(request.form['title'])
            title_elem.text = str(title_status)

        if 'reverse' in request.form:
            reverse_status = int(request.form['reverse'])
            reverse_elem.text = str(reverse_status)


        if 'period' in request.form:
            period_status = request.form['period']
            period_elem.text = str(period_status)

        if 'vBonus' in request.form:
            vBonus_status = int(request.form['vBonus'])
            vBonus_elem.text = str(vBonus_status)

        if 'hBonus' in request.form:
            hBonus_status = int(request.form['hBonus'])
            hBonus_elem.text = str(hBonus_status)

       


        tree = ET.ElementTree(root)
        tree.write('dashboard_data.xml')

    return render_template('basketball_dash.html', title=title_status, reverse=reverse_status, period=period_status, vBonus=vBonus_status, hBonus=hBonus_status)

if __name__ == '__main__':
    app.run()
