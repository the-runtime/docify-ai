import jedi


def find_references():
    env = jedi.create_environment("/home/tabish/Programming/PycharmProjects/docify-ai/venv2", safe=True)
    code = open("/home/tabish/Programming/PycharmProjects/docify-ai/docifyai/main.py", "r").read()

    script = jedi.Script(code=code, environment=env)
    # cursor = script.get_references(28, 13, include_builtins=False)
    # sdefin = script.goto(28, 35, follow_imports=True)
    # for defin in sdefin:
    #     print(defin.name)
    #     print(defin.module_path)
    #     print(defin.type)
        # if defin.type == "definition":
        #     print(defin.module_path if defin.module_path else "Unknown")
    name = script.search("clone_repo", all_scopes=True)
    for na in name:
        print(na.line, na.column, na.module_path)
    # print(name[0].defined_names())
    # cursor = script.get_names(all_scopes=True)
    # print(cursor)
    # references = [(r.module_path, r.line, r.column) for r in cursor]
    # return cursor


if __name__ == "__main__":
    references = find_references()
    # for ref in references:
    #     if ref.is_definition():
    #      print(f"References in {ref.module_path} at line {ref.line} at column {ref.column}")
