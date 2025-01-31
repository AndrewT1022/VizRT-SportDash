import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, jsonify
import threading
import time

from xml_combiner_soc.py import xmlCombine

app = Flask(__name__)

# Initialize the initial values of the toggle buttons
title_status = 0
reverse_status = 0
goal_status = 0  # 1 for HOME, 2 for AWAY
hCard_status = 0
vCard_status = 0
period_status = 0


# Create an initial XML structure
root = ET.Element('info')
title_elem = ET.SubElement(root, 'title')
reverse_elem = ET.SubElement(root, 'reverse')
goal_elem = ET.SubElement(root, 'goal')
vCard_elem = ET.SubElement(root, 'vCard')
hCard_elem = ET.SubElement(root, 'hCard')
period_elem = ET.SubElement(root, 'period')


def reset_goal():
    global goal_status
    time.sleep(5)  # Delay for 5 seconds, adjust as needed
    goal_status = 0
    goal_elem.text = str(goal_status)
    tree = ET.ElementTree(root)
    tree.write('dashboard_data.xml')  # Update the XML file


@app.route('/', methods=['GET', 'POST'])
def index():
    global title_status, goal_status, reverse_status, vCard_status, hCard_status, period_status

    if request.method == 'POST':
    
        if 'title' in request.form:
            title_status = int(request.form['title'])
            title_elem.text = str(title_status)

        if 'reverse' in request.form:
            reverse_status = int(request.form['reverse'])
            reverse_elem.text = str(reverse_status)

        if 'hGoal' in request.form:
            goal_status = 1
            goal_elem.text = str(goal_status)
            threading.Thread(target=reset_goal).start()  # Start the goal reset timer

        if 'vGoal' in request.form:
            goal_status = 2
            goal_elem.text = str(goal_status)
            threading.Thread(target=reset_goal).start()  # Start the goal reset timer

        if 'period' in request.form:
            period_status = request.form['period']
            period_elem.text = str(period_status)

        if 'vCard' in request.form:
            vCard_status = int(request.form['vCard'])
            vCard_elem.text = str(vCard_status)

        if 'hCard' in request.form:
            hCard_status = int(request.form['hCard'])
            hCard_elem.text = str(hCard_status)

       


        tree = ET.ElementTree(root)
        tree.write('dashboard_data.xml')

    return render_template('soccer_dash.html', title=title_status, goal=goal_status, reverse=reverse_status, period=period_status, vCard=vCard_status, hCard=hCard_status)

if __name__ == '__main__':
    app.run()
