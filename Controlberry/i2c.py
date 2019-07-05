import smbus

OPERATIONS = {"+":"__add__","/":'__rtruediv__', "-":"__sub__", "x":"__rmul__", "^":"__rxor__","<<":"__rlshift__", ">>":"__rshift__" }


def read_bytes(bus = 1, address = 0x00, bytes_to_send = 0, length_bytes_received = 2):
    """
    writes and return bytes
    """
    smb = smbus.SMBus(bus)
    bytes_returned = smb.read_i2c_block_data(address, bytes_to_send, length_bytes_received)
    return bytes_returned

example_operations = {0:[["x",128]], "total":[['/',1024]]}

def transform_bytes(bytes_list, operations):
    """
    transform received bytes by operations tuple, operations implemented: +-/* and bitewise >>, << and ^
    """
    total = False
    for i, item in enumerate(bytes_list):
        value = float(item)
        oper = operations.get(i)
        if oper:
            for o in oper:
                method = OPERATIONS[o[0]]
                function = getattr(float, method)
                val = float(o[1])
                value = function(val, value)
                total += value
        else:
            total += value
    if operations.get('total'):
        total = float(total)
        op = operations.get('total')
        if op:
            for o in op:
                method = OPERATIONS[o[0]]
                func = getattr(float, method)
                val = float(o[1])
                total = func(val, total)
    return total
