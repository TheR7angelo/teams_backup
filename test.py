import base64


def get_ext_from_byte(byte: bytes):
    byte = str(base64.b64encode(byte))

    if byte[2:12] == 'iVBORw0KGg':
        return '.png'
    elif byte[3:7] == '9j/4':
        return '.jpg'
    elif byte[2:6] == 'R0lG':
        return '.gif'
    elif byte[2:7] in ['SUkqA', 'TU0AK']:
        return '.tif'
    else:
        return '.txt'
