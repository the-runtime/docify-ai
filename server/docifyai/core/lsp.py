'''Not in use as of now '''

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
        params = {"processId": 3197, "clientInfo": {"name": "Code - OSS", "version": "1.83.0"}, "locale": "en",
         "rootPath": "/home/tabish/Programming/GolandProjects/serverDowndrive",
         "rootUri": "file:///home/tabish/Programming/GolandProjects/serverDowndrive", "capabilities": {
            "workspace": {"applyEdit": True, "workspaceEdit": {"documentChanges": True,
                                                               "resourceOperations": ["create", "rename", "delete"],
                                                               "failureHandling": "textOnlyTransactional",
                                                               "normalizesLineEndings": True,
                                                               "changeAnnotationSupport": {"groupsOnLabel": True}},
                          "configuration": True,
                          "didChangeWatchedFiles": {"dynamicRegistration": True, "relativePatternSupport": True},
                          "symbol": {"dynamicRegistration": True, "symbolKind": {
                              "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                           22, 23, 24, 25, 26]}, "tagSupport": {"valueSet": [1]},
                                     "resolveSupport": {"properties": ["location.range"]}},
                          "codeLens": {"refreshSupport": True}, "executeCommand": {"dynamicRegistration": True},
                          "didChangeConfiguration": {"dynamicRegistration": True}, "workspaceFolders": True,
                          "semanticTokens": {"refreshSupport": True},
                          "fileOperations": {"dynamicRegistration": True, "didCreate": True, "didRename": True,
                                             "didDelete": True, "willCreate": True, "willRename": True,
                                             "willDelete": True}, "inlineValue": {"refreshSupport": True},
                          "inlayHint": {"refreshSupport": True}, "diagnostics": {"refreshSupport": True}},
            "textDocument": {"publishDiagnostics": {"relatedInformation": True, "versionSupport": False,
                                                    "tagSupport": {"valueSet": [1, 2]}, "codeDescriptionSupport": True,
                                                    "dataSupport": True},
                             "synchronization": {"dynamicRegistration": True, "willSave": True,
                                                 "willSaveWaitUntil": True, "didSave": True},
                             "completion": {"dynamicRegistration": True, "contextSupport": True,
                                            "completionItem": {"snippetSupport": True, "commitCharactersSupport": True,
                                                               "documentationFormat": ["markdown", "plaintext"],
                                                               "deprecatedSupport": True, "preselectSupport": True,
                                                               "tagSupport": {"valueSet": [1]},
                                                               "insertReplaceSupport": True, "resolveSupport": {
                                                    "properties": ["documentation", "detail", "additionalTextEdits"]},
                                                               "insertTextModeSupport": {"valueSet": [1, 2]},
                                                               "labelDetailsSupport": True}, "insertTextMode": 2,
                                            "completionItemKind": {
                                                "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                                             18, 19, 20, 21, 22, 23, 24, 25]}, "completionList": {
                                     "itemDefaults": ["commitCharacters", "editRange", "insertTextFormat",
                                                      "insertTextMode"]}},
                             "hover": {"dynamicRegistration": True, "contentFormat": ["markdown", "plaintext"]},
                             "signatureHelp": {"dynamicRegistration": True, "signatureInformation": {
                                 "documentationFormat": ["markdown", "plaintext"],
                                 "parameterInformation": {"labelOffsetSupport": True}, "activeParameterSupport": True},
                                               "contextSupport": True},
                             "definition": {"dynamicRegistration": True, "linkSupport": True},
                             "references": {"dynamicRegistration": True},
                             "documentHighlight": {"dynamicRegistration": True},
                             "documentSymbol": {"dynamicRegistration": True, "symbolKind": {
                                 "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                              22, 23, 24, 25, 26]}, "hierarchicalDocumentSymbolSupport": True,
                                                "tagSupport": {"valueSet": [1]}, "labelSupport": True},
                             "codeAction": {"dynamicRegistration": True, "isPreferredSupport": True,
                                            "disabledSupport": True, "dataSupport": True,
                                            "resolveSupport": {"properties": ["edit"]}, "codeActionLiteralSupport": {
                                     "codeActionKind": {
                                         "valueSet": ["", "quickfix", "refactor", "refactor.extract", "refactor.inline",
                                                      "refactor.rewrite", "source", "source.organizeImports"]}},
                                            "honorsChangeAnnotations": False},
                             "codeLens": {"dynamicRegistration": True}, "formatting": {"dynamicRegistration": True},
                             "rangeFormatting": {"dynamicRegistration": True},
                             "onTypeFormatting": {"dynamicRegistration": True},
                             "rename": {"dynamicRegistration": True, "prepareSupport": True,
                                        "prepareSupportDefaultBehavior": 1, "honorsChangeAnnotations": True},
                             "documentLink": {"dynamicRegistration": True, "tooltipSupport": True},
                             "typeDefinition": {"dynamicRegistration": True, "linkSupport": True},
                             "implementation": {"dynamicRegistration": True, "linkSupport": True},
                             "colorProvider": {"dynamicRegistration": True},
                             "foldingRange": {"dynamicRegistration": True, "rangeLimit": 5000, "lineFoldingOnly": True,
                                              "foldingRangeKind": {"valueSet": ["comment", "imports", "region"]},
                                              "foldingRange": {"collapsedText": False}},
                             "declaration": {"dynamicRegistration": True, "linkSupport": True},
                             "selectionRange": {"dynamicRegistration": True},
                             "callHierarchy": {"dynamicRegistration": True},
                             "semanticTokens": {"dynamicRegistration": True,
                                                "tokenTypes": ["namespace", "type", "class", "enum", "interface",
                                                               "struct", "typeParameter", "parameter", "variable",
                                                               "property", "enumMember", "event", "function", "method",
                                                               "macro", "keyword", "modifier", "comment", "string",
                                                               "number", "regexp", "operator", "decorator"],
                                                "tokenModifiers": ["declaration", "definition", "readonly", "static",
                                                                   "deprecated", "abstract", "async", "modification",
                                                                   "documentation", "defaultLibrary"],
                                                "formats": ["relative"],
                                                "requests": {"range": True, "full": {"delta": True}},
                                                "multilineTokenSupport": False, "overlappingTokenSupport": False,
                                                "serverCancelSupport": True, "augmentsSyntaxTokens": True},
                             "linkedEditingRange": {"dynamicRegistration": True},
                             "typeHierarchy": {"dynamicRegistration": True},
                             "inlineValue": {"dynamicRegistration": True}, "inlayHint": {"dynamicRegistration": True,
                                                                                         "resolveSupport": {
                                                                                             "properties": ["tooltip",
                                                                                                            "textEdits",
                                                                                                            "label.tooltip",
                                                                                                            "label.location",
                                                                                                            "label.command"]}},
                             "diagnostic": {"dynamicRegistration": True, "relatedDocumentSupport": False}},
            "window": {"showMessage": {"messageActionItem": {"additionalPropertiesSupport": True}},
                       "showDocument": {"support": True}, "workDoneProgress": True}, "general": {
                "staleRequestSupport": {"cancel": True, "retryOnContentModified": ["textDocument/semanticTokens/full",
                                                                                   "textDocument/semanticTokens/range",
                                                                                   "textDocument/semanticTokens/full/delta"]},
                "regularExpressions": {"engine": "ECMAScript", "version": "ES2020"},
                "markdown": {"parser": "marked", "version": "1.1.0"}, "positionEncodings": ["utf-16"]},
            "notebookDocument": {"synchronization": {"dynamicRegistration": True, "executionSummarySupport": True}}},
         "initializationOptions": {"ui.inlayhint.hints": {"assignVariableTypes": False, "compositeLiteralFields": False,
                                                          "compositeLiteralTypes": False, "constantValues": False,
                                                          "functionTypeParameters": False, "parameterNames": False,
                                                          "rangeVariableTypes": False}, "ui.vulncheck": "Off"},
         "trace": "messages", "workspaceFolders": [
            {"uri": "file:///home/tabish/Programming/GolandProjects/serverDowndrive", "name": "serverDowndrive"}]}

        # ams = {
        #     "jsonrpc": "2.0",
        #     "id": 1,
        #     "method": "initialize",
        #     "workspace": {
        #         "workspaceFolders": [
        #             {
        #                 "uri": "file:///home/tabish/Programming/PycharmProjects/docify-ai/docifyai",
        #                 "name": "docifyai"
        #             },
        #         ],
        #         "extraPaths": [],
        #         "environmentPath": "~/home/tabish/Programming/PycharmProjects/docify-ai/venv2/bin/python",
        #         "symbols": {
        #             "ignoreFolders": [".nox", ".tox", ".venv", "__pycache__", "venv"],
        #             "maxSymbols": 20
        #         }
        #     },
        #
        #     "params": {
        #         "processId": 12345,
        #         # "rootPath": "/home/tabish/Programming/GolandProjects/serverDowndrive",
        #         # "rootUri": "file:///home/tabish/Programming/GolandProjects/serverDowndrive",
        #         "trace": "on",
        #         "capabilities": {
        #             "textDocument": {
        #                 "references": {
        #                     "dynamicRegistration": True
        #                 }
        #             }
        #         }
        #     }
        # }

        self.send_request(method, params)
        res = self.receive_response()
        print(res)

    def send_request(self, method, params):
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        }
        # request = params
        request_str = json.dumps(request)
        content_length = len(request_str)
        self.conn.sendall(f'Content-Length: {content_length}\r\n\r\n'.encode('utf-8'))
        self.conn.sendall(request_str.encode('utf-8'))

    # def receive_response(self):
    #     message = b''
    #     while True:
    #         res = self.conn.recv(1024)
    #         # print(res)
    #         if not res:
    #             break
    #         message += res
    #     print(message.decode())
    #     return message.decode()

    def receive_response(self):
        headers = {}
        i = 0
        hello = self.conn.makefile()
        # while True:
        #     line = hello.readline()
        #     print(str(i) + line)
        #     i += 1
        #     if line == '\r\n':
        #         print("breaks")
        #         break
        #     if line == "\n":
        #         continue
        #     header, value = line.split(':', 1)
        #     headers[header] = value.strip()
        # tabish
        while True:
            line = hello.readline()
            header, value = line.split(':', 1)
            headers[header] = value.strip()
            if line[len(line) - 1] == "\n":
                print("line break")
                break
        content_length = int(headers['Content-Length'])
        response_byte = self.conn.recv(content_length)
        response_str = response_byte.decode('utf-8')
        return json.loads(response_str)

    def find_references(self, text_document, position):
        self.send_request('textDocument/completion', {
            'processId': 3197,
            'textDocument': text_document,
            'position': position,
            'context': {'includeDeclaration': True}
        })

        return self.receive_response()

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
            if token_type in Token.Literal:
                # if token[0] in lexer.tokens['root']:
                print("token: ", token, "line, char: ", line_number, " ", char_number)
                # references = self.find_references({'uri': file_uri}, {'line': token[2][0], 'character': token[2][1]})
                references = self.find_references({'uri': file_uri}, {'line': line_number, 'character': char_number})
                if references:
                    # print(f'References at line {token[2][0] + 1}, character {token[2][1] + 1}:')
                    print(references)
            if token == "\n":
                last_char = temp_char
                line_number += 1
                tabs = 0

    def stats_call(self):
        method = 'notification/initialized'
        # workspace_folders = [
        #     {
        #         "uri": "file:///home/tabish/Programming/GolandProjects/serverDowndrive",
        #         "name": "serverDowndrive"
        #     }
        # ]
        params = {
            # "event": {
            #     "added": workspace_folders,
            #     "removed": []
            # }
        }
        # params = {}
        self.send_request(method, params)
        res = self.receive_response()
        print(res)


def main():
    client = LSPClient()
    client.connect()
    client.stats_call()
    client.analyze_file('file:///home/tabish/Programming/GolandProjects/serverDowndrive/main.go')


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    main()
