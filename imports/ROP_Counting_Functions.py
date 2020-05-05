import re

# -------------------
# -----FUNCTIONS-----
# -------------------

# return how many registers are used for given instructions
# special cases:
# return may be 0 or 1 depending on stack adjustment
# imul can be 0, 1,2 or 3 depending on usage

def get_inst_op_count(inst):
	inst = inst.lower()

	op_0 = ['aas', 'clc', 'leave', 'ret', 'retf', 'cld', 'daa', 'nop']
	op_1 = ['pop', 'push', 'call', 'inc', 'dec', 'idiv', 'jmp', 'not', 'neg', 'je', 'jne', 'jz', 'jg', 'jge', 'jl', 'jle']
	op_2 = ['add', 'mov', 'adc', 'xchg', 'lea', 'and', 'cmp', 'xor', 'sub', 'or', 'shl', 'shr']
	op_3 = ['imul']

	if inst in op_0:
		return 0
	elif inst in op_1:
		return 1
	elif inst in op_2:
		return 2
	else:
		return -1 # If not in list return negitive for error

def count_register_use(g_array):
	registers = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0}
	
	for r in registers:
		for i in g_array:
			for j in i['Gadget']:
				if j.find(r) >= 0:
					registers[r] += 1
	return registers


def count_derefrenced_registers(g_array, s_or_d):
	registers = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0}

	for r in registers:
		if s_or_d == "source" or s_or_d == "s":
			search_start = "[" + r
			search_end = "],"
		elif s_or_d == "destination" or s_or_d == "d":
			search_start = "[" + r
			search_end = "] "

		for i in g_array:
			for j in i['Gadget']:
				if j.find(search_start) >= 0 and j.find(search_end) >= 0:
					registers[r] += 1
	return registers

def count_instruction_reg(g_array, instruction):
	registers = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0, '0x':0}
	ops = get_inst_op_count(instruction)
	if ops == 0:
		return count_instruction(g_array, instruction)

	if ops == 1:
		inst_re = " " + instruction + " "
		for r in registers:
			reg_inst_re = inst_re + r
			for i in g_array:
				for j in i['Gadget']:
					if re.search(reg_inst_re, j) is not None:
						registers[r] += 1
		return registers
	elif ops == 2:
		source_reg = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0, '[0-9].*':0, 'byte':0, 'dword':0, 'other':0}
		dest_reg   = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0, '[0-9].*':0, 'byte ':0, 'dword':0, 'other':0}

		# inst_re = " " + instruction + " "

		# search dest regs
		for r in dest_reg.keys():
			# matches "<instruction> <register>," for source
			reg_inst_re = " " + instruction + " " + r
			for i in g_array:
				for j in i['Gadget']:
					if re.search(reg_inst_re, j) is not None: # check if regular expression matches instruction
						dest_reg[r] += 1

		source_reg['other'] = count_instruction(g_array, instruction) - sum(source_reg.values())
		# source_reg.pop('other')

		# search source
		for r in source_reg.keys():
			# matches "<instruction> <Anything>, <register>" for destination
			reg_inst_re = " " + instruction + " .*, " + r
			for i in g_array:
				for j in i['Gadget']:
					if re.search(reg_inst_re, j) is not None: # check if regular expression matches instruction
						source_reg[r] += 1

		# catch everything else without a regular expression
		# Included now:
		#   -segment registers
		#   -non-extended registers
		dest_reg['other'] = count_instruction(g_array, instruction) - sum(dest_reg.values())


		# Rename the dictionary keys that are regular expre
		source_reg['Constant'] = source_reg.pop('[0-9].*')
		dest_reg['Constant'] = dest_reg.pop('[0-9].*')

		source_reg['other'] = 0
		dest_reg['other'] = 0

		result = {"Source":source_reg,"Destination":dest_reg}
		return result
	else:
		print("The instruction was wrong or something")
		return 0


# total instruction use disreguarding registers
def count_instruction(g_array, instruction):
	# spaces ensure it is not part of another instruction
	inst_re = " " + instruction + " "
	count = 0

	for i in g_array:
		for j in i['Gadget']:
			if re.search(inst_re, j) is not None:
				count += 1

	# if re.search(inst_re)
	return count

# --------------
# -----MAIN-----
# --------------
# path = "C:\\Users\\User\\Desktop\\Rop_testing\\Gadget_sets\\"
# file_name = "one_variable.txt"

# gadget_list = prepare_gadgets(path + file_name)

# print(gadget_list[67][1])

# print(count_instruction(gadget_list, 'add'))
# a = count_instruction_reg(gadget_list, 'mov')
# print(a['Source'])
# print("---------------------------------------------")
# print(a['Destination'])
# print("---------------------------------------------")

# Graphing_functions.graph_binary_gadgets(a['Source'], a['Destination'], "Mov Usage")