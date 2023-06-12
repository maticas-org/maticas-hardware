# Complete project details at https://RandomNerdTutorials.com
import json


def web_page():

    with open("config.json", 'r') as f:
        current_settings = json.load(f)


    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>Maticas control</title>
    </head>
    <body>
    <h1>Maticas control</h1>
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
            <td><input type="time" id="lights-starttime"></td>
            <td><input type="time" id="lights-endtime"></td>
            <td>
                <select id="lights-type" onchange="toggleTimedFields('lights')">
                    <option value="on/off">On/Off</option>
                    <option value="timed">Timed</option>
                </select>
            </td>
            <td><input type="number" id="lights-minutes-off" disabled></td>
            <td><input type="number" id="lights-minutes-on" disabled></td>
        </tr>
        <tr>
            <td>Fan</td>
            <td><input type="time" id="fan-starttime"></td>
            <td><input type="time" id="fan-endtime"></td>
            <td>
                <select id="fan-type" onchange="toggleTimedFields('fan')">
                    <option value="on/off">On/Off</option>
                    <option value="timed">Timed</option>
                </select>
            </td>
            <td><input type="number" id="fan-minutes-off" disabled></td>
            <td><input type="number" id="fan-minutes-on" disabled></td>
        </tr>
        <tr>
            <td>Water Pump</td>
            <td><input type="time" id="waterpump-starttime"></td>
            <td><input type="time" id="waterpump-endtime"></td>
            <td>
                <select id="waterpump-type" onchange="toggleTimedFields('waterpump')">
                    <option value="on/off">On/Off</option>
                    <option value="timed">Timed</option>
                </select>
            </td>
            <td><input type="number" id="waterpump-minutes-off" disabled></td>
            <td><input type="number" id="waterpump-minutes-on" disabled></td>
        </tr>
        <tr>
            <td>Oxygen</td>
            <td><input type="time" id="oxygen-starttime"></td>
            <td><input type="time" id="oxygen-endtime"></td>
            <td>
                <select id="oxygen-type" onchange="toggleTimedFields('oxygen')">
                    <option value="on/off">On/Off</option>
                    <option value="timed">Timed</option>
                </select>
            </td>
            <td><input type="number" id="oxygen-minutes-off" disabled></td>
            <td><input type="number" id="oxygen-minutes-on" disabled></td>
        </tr>
        <tr>
            <td>Recirculation</td>
            <td><input type="time" id="recirculation-starttime"></td>
            <td><input type="time" id="recirculation-endtime"></td>
            <td>
                <select id="recirculation-type" onchange="toggleTimedFields('recirculation')">
                    <option value="on/off">On/Off</option>
                    <option value="timed">Timed</option>
                </select>
            </td>
            <td><input type="number" id="recirculation-minutes-off" disabled></td>
            <td><input type="number" id="recirculation-minutes-on" disabled></td>
        </tr>
    </table>

    <button onclick="saveData()">Save</button>

    <script>

        // Initialize the form values
        var initialValues = {
    """ + """lights: {
                type: "timed",
                starttime: [8, 0, 0],
                endtime: [17, 30, 0],
                minutes_off: 10,
                minutes_on: 20
            },
            fan: {
                type: "on/off",
                starttime: [9, 15, 0],
                endtime: [18, 45, 0],
                minutes_off: 0,
                minutes_on: 0
            },
            waterpump: {
                type: "timed",
                starttime: [10, 30, 0],
                endtime: [16, 45, 0],
                minutes_off: 5,
                minutes_on: 10
            },
            oxygen: {
                type: "on/off",
                starttime: [7, 0, 0],
                endtime: [22, 0, 0],
                minutes_off: 0,
                minutes_on: 0
            },
            recirculation: {
                type: "timed",
                starttime: [11, 0, 0],
                endtime: [15, 30, 0],
                minutes_off: 5,
                minutes_on: 15
            }
        };"""+ """
        // Function to set the initial form values
        function setInitialValues() {
            for (var key in initialValues) {
                if (initialValues.hasOwnProperty(key)) {
                    var actuator = initialValues[key];
                    document.getElementById(key + "-type").value = actuator.type;
                    document.getElementById(key + "-starttime").value = formatTime(actuator.starttime);
                    document.getElementById(key + "-endtime").value = formatTime(actuator.endtime);
                    document.getElementById(key + "-minutes-off").value = actuator.minutes_off;
                    document.getElementById(key + "-minutes-on").value = actuator.minutes_on;
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
            var data = {
                wifi_ssid: "Aulas EICT",
                wifi_password: "eict1234",
                actuators: {}
            };

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

        // Function to toggle visibility of timed fields
        function toggleTimedFields(actuator) {
            var typeSelect = document.getElementById(actuator + "-type");
            var minutesOffInput = document.getElementById(actuator + "-minutes-off");
            var minutesOnInput = document.getElementById(actuator + "-minutes-on");

            if (typeSelect.value === "timed") {
                minutesOffInput.disabled = false;
                minutesOnInput.disabled = false;
            } else {
                minutesOffInput.disabled = true;
                minutesOnInput.disabled = true;
            }
        }

        // Set the initial form values
        setInitialValues();
    </script>
    </body>
    </html>
    """

    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')

    led.value(1)
    if led_off == 6:
        print('LED OFF')
    led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

