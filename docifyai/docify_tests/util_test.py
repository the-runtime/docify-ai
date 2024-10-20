from docifyai.utils import utils

if __name__ == '__main__':
    text = '''this is not what 
        ```{
        "tabish": "hello",  
        "hassan": "world"
        }```  
        i want in here
    '''
    ret = utils.get_code_from_gpt_response(text)
    print(ret["tabish"])
