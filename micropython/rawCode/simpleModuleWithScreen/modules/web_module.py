try:
  import usocket as socket
except:
  import socket

import network
from html.parsers import parse_update_response


class WebModule:

    def __init__(self, config_file):
        self.config_file = config_file
        self.need_to_update = False
        self.start_web_server()

    def start_web_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(5)
        self.s.bind(('', 80))
      
    def serve(self):

        try:
          self.s.listen(5)
          conn, addr = self.s.accept()
        except OSError as e:
          if e.args[0] == 110:
            print("OSError: [Errno 110] ETIMEDOUT")
            return
          else:
            raise e

        print('Got a connection from %s' % str(addr))
        request = str(conn.recv(1024))
        print('Content = %s' % request)

        response = self.answer_request(request)

        if response == None:
            conn.send('HTTP/1.1 404 Not Found\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.close()
            return
        
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        
    def answer_request(self, response)->str:

        if response.find("GET /updateConfig ") != -1 :
            from html.pages import update_config
            return update_config

        elif response.find("GET / ") != -1:
            from html.pages import show_config
            return show_config(config_file=self.config_file)
        
        elif response.find("POST /update ") != -1:
            from html.pages import show_config
            from utils.json_related import update_json_actuator
            
            update_json_actuator(self.config_file, "0", parse_update_response(response))
            self.need_to_update = True

            return show_config(config_file=self.config_file)

        # Add more conditions for other paths if needed
        else:
            return None

