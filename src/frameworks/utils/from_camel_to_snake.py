import re

def from_camel_to_snake(item):
    map_item = {**item}
    for key in list(map_item.keys()):
        new_key = camel_to_snake(key)
        if isinstance(map_item[key], list):
            map_item[key] = [from_camel_to_snake(subitem) for subitem in map_item[key]]
        elif isinstance(map_item[key], dict) and not isinstance(map_item[key], datetime.date) and map_item[key] is not None:
            map_item[key] = from_camel_to_snake(map_item[key])
        map_item[new_key] = map_item[key]
        if key != new_key:
            del map_item[key]
    return map_item

def camel_to_snake(string):
    return re.sub(r'([A-Z])', r'_\1', string).lower()