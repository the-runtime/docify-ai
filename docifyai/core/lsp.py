import asyncio
import json
import socket
from pygments.lexers import get_lexer_by_name
from pygments import lex
from pygments.token import Token


class LSPClient:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.conn = None


    def connect(self):
        self.conn = socket.create_connection((self.host, self.port))
        method = "initialize"
        params = {
            "processId": 1,
            "rootUri": "file:///home/tabish/Programming/GolandProjects/serverDowndrive",
            "capabilities": {
                "workspace": {
                    "workspaceFolders": True
                },
                "textDocument": {
                    "synchronization": {
                        "willSave": True,
                        "willSaveWaitUntil": True,
                        "didSave": True
                    },
                    "completion": {
                        "completionItem": {
                            "snippetSupport": True,
                            "commitCharactersSupport": True
                        }
                    }
                }
            }
        }

        self.send_request(method, params)
        res = self.receive_response()

    def send_request(self, method, params):
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        }
        request_str = json.dumps(request)
        content_length = len(request_str)
        self.conn.sendall(f'Content-Length: {content_length}\r\n\r\n'.encode('utf-8'))
        self.conn.sendall(request_str.encode('utf-8'))

    def receive_response(self):
        message = b''
        while True:
            res = self.conn.recv(1024)
            print(res)
            if not res:
                break
            message += res
        print(message.decode())
        return message.decode()

    # def receive_response(self):
    #     headers = {}
    #     i = 0
    #     # response_json = self.conn.recv(1024).decode()
    #     # print(response_json)
    #     # response = json.loads(response_json)
    #     # print(response)
    #     while True:
    #         line = self.conn.makefile().readline()
    #         print(str(i) + line)
    #         i += 1
    #         if line == '\r\n':
    #             print("breks")
    #             break
    #         header, value = line.split(':', 1)
    #         headers[header] = value.strip()
    #     content_length = int(headers['Content-Length'])
    #     response_str = self.conn.recv(content_length).decode('utf-8')
    #     return json.loads(response_str)

    def find_references(self, text_document, position):
        self.send_request('textDocument/references', {
            'textDocument': text_document,
            'position': position,
            'context': {'includeDeclaration': True}
        })

    # return self.receive_response()

    def analyze_file(self, file_uri):
        # Assuming the file is small and can be read all at once
        with open(file_uri[7:], 'r') as f:  # Remove 'file://' from the URI
            source_code = f.read()

        lexer = get_lexer_by_name("go")
        # tokens = list(lex(source_code, lexer))
        tokens = list(lexer.get_tokens_unprocessed(source_code))

        line_number = 1
        last_char = 0
        tabs = 0
        for index, token_type, token in tokens:
            # if token == "\t":
            #     char_number = index - last_char + 4
            #     tabs += 4
            # else:
            char_number = index - last_char

            # if (token != "\t" or "\n"):
            #     temp_char = index + len(token) - 1
            temp_char = index + len(token)
            if token_type in Token.Keyword:
                # if token[0] in lexer.tokens['root']:
                print("token: ", token)
                # references = self.find_references({'uri': file_uri}, {'line': token[2][0], 'character': token[2][1]})
                references = self.find_references({'uri': file_uri}, {'line': line_number, 'character': char_number})
                if references:
                    # print(f'References at line {token[2][0] + 1}, character {token[2][1] + 1}:')
                    print(references)
            if token == "\n":
                last_char = temp_char
                line_number += 1
                tabs = 0


def main():
    client = LSPClient()
    client.connect()
    # client.analyze_file('file:///home/tabish/Programming/GolandProjects/serverDowndrive/main.go')


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    main()
