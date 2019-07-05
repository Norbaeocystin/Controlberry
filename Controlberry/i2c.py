import smbus

bus = smbus.SMBus(1)

OPERATIONS = {"+":"__add__","/":'__rtruediv__', "-":"__sub__", "x":"__rmul__", 
	"^":"__rxor__","<<":"__rlshift__", ">>":"__rshift__" }

def write_byte_to_address(bus = 1, byte = 0, address = 0x00):
	smb = smbus.SMBus(bus)
	smb.write_byte(address, byte)

def read_bytes(bus = 1, address = 0x00, bytes_to_send = 0, length_bytes_received = 2):
	"""

	"""
	smb = smbus.SMBus(bus)
	bytes_returned = smb.read_i2c_block_data(address, bytes_to_send, length_bytes_received)
	return bytes_returned

example_operations = {0:[["x",128]], "total":[["/",1024"]]}
def transform_bytes(bytes, operations = {0:[["+",2], ['/', 3]]}):
	total = False
	for i, item in enumerate(bytes):
		value = item
		oper = operations.get(i):
		if oper:
			for o in oper:
				method = OPERATIONS[o[0]]
				function = float.getattr(method)
				value = function(value, o[1])
		total += value
	if operations.get('total'):
		oper = operations.get(i):
		if oper:
			for o in oper:
				method = OPERATIONS[o[0]]
				function = float.getattr(method)
				total = function(value, o[1])
	return total
		

