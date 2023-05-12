import json
import re


def convert_to_json(data):
    data = re.sub(r'(\w+)=(\w+)', r'"\1": \2', data)
    data = re.sub(r'(\w+)=(\d+)', r'"\1": \2', data)
    data = re.sub(r'=', r':', data)

  
    return data





if __name__ == '__main__':
    # data = "m762_zl = {{x=0, y=3, d=2}, {x=0, y=2, d=2}}"
    data = ""
    json_data = convert_to_json(data)
    print(json_data)

