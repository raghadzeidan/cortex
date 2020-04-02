import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.server
import socketserver
import sys
PORT = 8000
#TODO: see what website.py did in exercise 2, and fix run_webserver command
Handler = http.server.SimpleHTTPRequestHandler
_INDEX_HTML = '''
<html>
    <head>
        <title>
            Interface of some sort.
        </title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_PAGE_TEMPLATE= '''
<html>
    <head>
        <title>Brain Computer Interface: User {number}</title>
    </head>
    <body>
        <table>
            {user_thought}
        </table>
    </body>
</html>

'''

_USER_THOUGHT = '''
            <tr>
                <td>{time}</td>
                <td>{thought}</td>
            </tr>
'''

users_html = []
users_page_html = {}
index_html = ''
thoughts_html = {}
ERROR_SERVER = 'Error'
static_dir = ''
def flush():
    global users_html
    global users_page_html
    global index_html
    global thoughts_html
    users_html = []
    users_page_html = {}
    index_html = ''
    thoughts_html = {}
def load_dynamically():
    global static_dir
    global users_html
    global users_page_html
    global index_html
    global thoughts_html
    data_dir = static_dir
    for user_dir in os.listdir(data_dir):
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir))
        full_user_dir_path = data_dir + '/' + user_dir
        thoughts_html[user_dir]=[]
        users_page_html[user_dir] = ''
        for thought_time_file in os.listdir(full_user_dir_path):
            full_thought_path = full_user_dir_path + '/' + thought_time_file
            with open(full_thought_path, mode = 'r') as thought_time:
                time_of_current_thought_array = thought_time_file.split('_')
                time_of_curent_thought = time_parse(time_of_current_thought_array)
                for line in thought_time.readlines():
                    thoughts_html[user_dir].append(_USER_THOUGHT.format(time = time_of_curent_thought, thought=line))
        users_page_html[user_dir] = _USER_PAGE_TEMPLATE.format(number = user_dir, user_thought = '\n'.join(thoughts_html[user_dir]))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))

class Serv(BaseHTTPRequestHandler):
    global index_html
    global users_page_html
    global users_html
    html = ''
    def do_GET(self):
        if self.path == '/':
            html = index_html
            self.send_response(200)
        elif self.path[:7] == '/users/':
            flush()
            load_dynamically()
            html = users_page_html[self.path[7:]]
            self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(html,'utf-8'))
def time_parse(array):
    return array[0] + ' ' + array[1].replace('-',':')[:-4]

def run_webserver(address_arg, data_dir):
    global index_html
    global users_html
    global users_page_html
    global thoughts_html
    global static_dir
    address = adress_arg.split(':')
    ip, port = address
    static_dir = data_dir
    load_dynamically()
    httpd = HTTPServer((ip, port),Serv)
    httpd.serve_forever()

if __name__ == '__main__':
    run_webserver(sys.argv[1], sys.argv[2])

