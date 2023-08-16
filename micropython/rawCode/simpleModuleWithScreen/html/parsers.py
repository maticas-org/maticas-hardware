def unquote_to_str(string) -> str:
    """
    unquote_to_str('abc%20def') -> 'abc def'.
    Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.
    """
    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    def hex_to_byte(hex_chars):
        return bytes([int(hex_chars, 16)])

    res = bytearray()
    idx = 0
    length = len(string)

    while idx < length:
        if string[idx] == ord('%'):
            if idx + 2 < length and chr(string[idx + 1]) in '0123456789ABCDEFabcdef' and chr(string[idx + 2]) in '0123456789ABCDEFabcdef':
                hex_chars = chr(string[idx + 1]) + chr(string[idx + 2])
                res.extend(hex_to_byte(hex_chars))
                idx += 3
            else:
                res.append(ord('%'))
                idx += 1
        elif string[idx] == ord('+'):
            res.append(ord(' '))
            idx += 1
        else:
            res.append(string[idx])
            idx += 1

    return res.decode('utf-8')




def parse_update_response(response: str) -> dict:
    
    """
        Given a response from the web server, this function parses it and returns a dict with the values.
        Response is similar to this:
        "POST /update?name=light&starttime=00:00&endtime=00:00&type=on&minuteson=0&minutesoff=0 HTTP/1.1"

        This function returns a dict with the following keys:
        name, starttime, endtime, type, minuteson, minutesoff
    """

    start_idx = response.find("name=")
    end_idx = response.find("&", start_idx)
    name = response[start_idx+len("name="):end_idx]
    
    start_idx = response.find("starttime=")
    end_idx = response.find("&", start_idx)
    starttime = response[start_idx+len("starttime="):end_idx]
    
    start_idx = response.find("endtime=")
    end_idx = response.find("&", start_idx)
    endtime = response[start_idx+len("endtime="):end_idx]
    
    start_idx = response.find("type=")
    end_idx = response.find("&", start_idx)
    type_ = response[start_idx+len("type="):end_idx]
    
    start_idx = response.find("minuteson=")
    end_idx = response.find("&", start_idx)
    minuteson = response[start_idx+len("minuteson="):end_idx]
    
    start_idx = response.find("minutesoff=")
    end_idx = response.find("'", start_idx)
    minutesoff = response[start_idx+len("minutesoff="):end_idx]
    
    from utils.time_management_module import Time
    
    return {
        "name":unquote_to_str(name),
        "starttime": Time.from_string_to_list(unquote_to_str(starttime)),
        "endtime": Time.from_string_to_list(unquote_to_str(endtime)),
        "type": unquote_to_str(type_),
        "minuteson": int(unquote_to_str(minuteson)),
        "minutesoff": int(unquote_to_str(minutesoff))
    }

