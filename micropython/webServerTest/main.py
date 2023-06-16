try:
  import usocket as socket
except:
  import socket
  
# Complete project details at https://RandomNerdTutorials.com
import json
import network
from internet_connection import reconnect

def extract_form_data(request_content):
    # Extract the form data from the request content
    data = {}
    fields = request_content.split('&')
    for field in fields:
        key_value = field.split('=')
        key = key_value[0]
        value = key_value[1]
        data[key] = value
    return data

def web_page():

    CURRENT_SETTINGS = {}
    
    with open("config.json", 'r') as f:
        CURRENT_SETTINGS = json.load(f)

    html = """<!DOCTYPE html>
        <html>
        <head>
        <title>Maticas control</title>
        </head>
        <body>
        <h1>Maticas control</h1>

        <form action="/" method="POST">
        <table>
            <tr>
                <th>Actuator</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Actuator Type</th>
                <th>Minutes Off</th>
                <th>Minutes On</th>
            </tr>
            <tr>
                <td>Lights</td>
                <td><input type="time" id="lights-starttime" name="lights-starttime"></td>
                <td><input type="time" id="lights-endtime" name="lights-endtime"></td>
                <td>
                    <select id="lights-type" name="lights-type" onchange="toggleTimedFields('lights')">
                        <option value="on/off">On/Off</option>
                        <option value="timed">Timed</option>
                    </select>
                </td>
                <td><input type="number" id="lights-minutes-off" name="lights-minutes-off" disabled></td>
                <td><input type="number" id="lights-minutes-on" name="lights-minutes-on" disabled></td>
            </tr>
            <tr>
                <td>Fan</td>
                <td><input type="time" id="fan-starttime" name="fan-starttime"></td>
                <td><input type="time" id="fan-endtime" name="fan-endtime"></td>
                <td>
                    <select id="fan-type" name="fan-type" onchange="toggleTimedFields('fan')">
                        <option value="on/off">On/Off</option>
                        <option value="timed">Timed</option>
                    </select>
                </td>
                <td><input type="number" id="fan-minutes-off" name="fan-minutes-off" disabled></td>
                <td><input type="number" id="fan-minutes-on" name="fan-minutes-on" disabled></td>
            </tr>
            <tr>
                <td>Water Pump</td>
                <td><input type="time" id="waterpump-starttime" name="waterpump-starttime"></td>
                <td><input type="time" id="waterpump-endtime" name="waterpump-endtime"></td>
                <td>
                    <select id="waterpump-type" name="waterpump-type" onchange="toggleTimedFields('waterpump')">
                        <option value="on/off">On/Off</option>
                        <option value="timed">Timed</option>
                    </select>
                </td>
                <td><input type="number" id="waterpump-minutes-off" name="waterpump-minutes-off" disabled></td>
                <td><input type="number" id="waterpump-minutes-on" name="waterpump-minutes-on" disabled></td>
            </tr>
            <tr>
                <td>Oxygen</td>
                <td><input type="time" id="oxygen-starttime" name="oxygen-starttime"></td>
                <td><input type="time" id="oxygen-endtime" name="oxygen-endtime"></td>
                <td>
                    <select id="oxygen-type" name="oxygen-type" onchange="toggleTimedFields('oxygen')">
                        <option value="on/off">On/Off</option>
                        <option value="timed">Timed</option>
                    </select>
                </td>
                <td><input type="number" id="oxygen-minutes-off" name="oxygen-minutes-off" disabled></td>
                <td><input type="number" id="oxygen-minutes-on" name="oxygen-minutes-on" disabled></td>
            </tr>
            <tr>
                <td>Recirculation</td>
                <td><input type="time" id="recirculation-starttime" name="recirculation-starttime"></td>
                <td><input type="time" id="recirculation-endtime" name="recirculation-endtime"></td>
                <td>
                    <select id="recirculation-type" name="recirculation-type" onchange="toggleTimedFields('recirculation')">
                        <option value="on/off">On/Off</option>
                        <option value="timed">Timed</option>
                    </select>
                </td>
                <td><input type="number" id="recirculation-minutes-off" name="recirculation-minutes-off" disabled></td>
                <td><input type="number" id="recirculation-minutes-on" name="recirculation-minutes-on" disabled></td>
            </tr>
        </table>

        <input type="submit" value="Submit">
        </form> 



        <script>

            // Initialize the form values
            var initialValues = """+ str(CURRENT_SETTINGS["actuators"]) + ";" +"""

            // Function to toggle visibility of timed fields
            function toggleTimedFields(actuator) {
                var typeSelect = document.getElementById(actuator + "-type");
                var minutesOffInput = document.getElementById(actuator + "-minutes-off");
                var minutesOnInput = document.getElementById(actuator + "-minutes-on");

                if (typeSelect.value == "timed"){
                    minutesOffInput.disabled = false;
                    minutesOnInput.disabled = false;
                } else {
                    minutesOffInput.disabled = true;
                    minutesOnInput.disabled = true;
                }
            }

            // Function to set the initial form values
            function setInitialValues() {
                for (var key in initialValues) {
                    if (initialValues.hasOwnProperty(key)) {
                        var actuator = initialValues[key];

                        document.getElementById(key + "-type").value                = actuator.type;
                        document.getElementById(key + "-starttime").value   = formatTime(actuator.starttime);
                        document.getElementById(key + "-endtime").value     = formatTime(actuator.endtime);
                        toggleTimedFields(key);
                        document.getElementById(key + "-minutes-off").value = parseInt(actuator.minutes_off);
                        document.getElementById(key + "-minutes-on").value  = parseInt(actuator.minutes_on);
                    }    
                }
            }
            

            // Function to format time values
            function formatTime(timeArray) {
                return ("0" + timeArray[0]).slice(-2) + ":" +
                       ("0" + timeArray[1]).slice(-2) + ":" +
                       ("0" + timeArray[2]).slice(-2);
            }

            // Function to save the form data
            function saveData() {
                // Retrieve the current values from the form
                var data = initialValues;

                for (var key in initialValues) {
                    if (initialValues.hasOwnProperty(key)) {
                        var actuator = initialValues[key];
                        data.actuators[key] = {
                            type: document.getElementById(key + "-type").value,
                            starttime: parseTime(document.getElementById(key + "-starttime").value),
                            endtime: parseTime(document.getElementById(key + "-endtime").value),
                            minutes_off: parseNumber(document.getElementById(key + "-minutes-off").value),
                            minutes_on: parseNumber(document.getElementById(key + "-minutes-on").value)
                        };
                    }
                }

                // Function to parse time inputs
                function parseTime(input) {
                    var timeParts = input.split(":");
                    return [parseInt(timeParts[0]), parseInt(timeParts[1]), parseInt(timeParts[2])];
                }

                // Function to parse number inputs
                function parseNumber(input) {
                    return input ? parseInt(input) : 0;
                }

                // Display the JSON data
                alert(JSON.stringify(data, null, 2));
            }


            // Set the initial form values
            setInitialValues();
        </script>
        </body>
        </html>
        """

    return html

#connect2(config_file = "config.json")
#connect2(config_file = "config.json", doreconnect = True)
#reconnect(config_file = "config.json", sta_if = network.WLAN(network.STA_IF))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)


    if request.find('POST') != -1:
        # Find the start and end index of the request content
        start_index = request.find(r';q=0.9\r\n\r\n') + 14
        print("\n\n START INDEX:", start_index)
        
        if start_index != -1:
            request_content = request[start_index:]
            print("\n\n\n GOT:", request_content)
            
            form_data = extract_form_data(request_content)
            print("\n\n\n FORM DATA:", form_data)

            save_form_data(form_data)


    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

