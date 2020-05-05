import re

def process_rop_file(path):

	gad_list = []
	single_gad = {}

	f = open(path, 'r')
	gadgets = f.read()
	gadgets = gadgets.split('\n')

	for g in gadgets:
		# print(g)
		if g == "":
			break

		single_gad = {}
		i = g.split('|') 

		# fill dictionay with each part from list
		single_gad['Module'] = i[0]
		single_gad['Address'] = i[1]
		single_gad['Gadget'] = i[2].split(';') # gadget split into instrutions

		if single_gad['Gadget'][len(single_gad['Gadget']) -1].find('ret') >= 0:
			if single_gad['Gadget'][len(single_gad['Gadget']) -1].find('retf') < 0: 
				gad_list.append(single_gad) # make sure gadget ends in return and not far return or anything else
	f.close()
	return gad_list



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

def count_register_use(g_array):
	registers = {'eax': 0, 'ebx':0, 'ecx':0, 'edx':0, 'edi':0, 'esi':0, 'esp':0, 'ebp':0}
	
	for r in registers:
		for i in g_array:
			for j in i['Gadget']:
				if j.find(r) >= 0:
					registers[r] += 1
	return registers

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


# ---- TESTING ----#
#- delete before making import

# a = process_rop_file("C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\Easy MPEG to DVD Burner.exe_ROP\\Easy MPEG to DVD Burner.exe_ROP_Gadgets.txt")

# print(count_derefrenced_registers(a, 'd'))