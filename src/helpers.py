import binascii

def bytes_to_hexstr(x: dict | bytes | list[bytes]) -> str | list[str] | dict:
    """
    Converts bytes to hexstring
    """
    if isinstance(x, dict):
        new_dict = {}
        for k, v in x.items():
            new_dict[bytes_to_hexstr(k)] = bytes_to_hexstr(v)
        return new_dict
    if isinstance(x, list):
        return [bytes_to_hexstr(i) for i in x]
    if isinstance(x, bytes):
        return "0x" + binascii.hexlify(x).decode().lower()
    return x

def hexstr_to_bytes(x: any) -> list[bytes] | bytes:
    """
    Converts hexstring to bytes
    """
    if isinstance(x, dict):
        new_dict = {}
        for k, v in x.items():
            new_dict[hexstr_to_bytes(k)] = hexstr_to_bytes(v)
        return new_dict
    if isinstance(x, list):
        return [hexstr_to_bytes(i) for i in x]
    if isinstance(x, str):
        try:
            return bytes.fromhex(x.replace("0x", ""))
        except:
            return x
    return x

