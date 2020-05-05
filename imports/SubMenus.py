from imports.Processes import *
from imports.Rop_File_Intake import *
from imports.Graphing_functions import *
from imports.ROP_Counting_Functions import *
from imports.Count_Side_Effects import *
from imports.Chain_Generator import *
from imports.SubMenus import *

from cmd import Cmd

class graphing_menu(Cmd):
	def __init__(self, r):
		Cmd.__init__(self)
		self.rop_list = r

	def emptyline(self):
		pass

	def do_exit(self, args):
		print("Return to main menu")
		return True

	# returns multiple arguments as a list, changes any strings that are ints to type int
	def process_multi_args(self, args):
		args = args.split()    
		for i, arg in enumerate(args):
			if arg.isdigit():
				args[i] = int(args[i])
		return args

	def do_registers(self, args):
		"""Graph all occurances of every register in the binary"""
		a = count_register_use(self.rop_list)
		graph_registers(a, "All Registers.")

	def do_instruction(self, args):
		"""Graph all occurances of an instruction. Gives source and destination if applicable."""
		args = self.process_multi_args(args)

		if len(args) == 1: # arg is 
			args = args[0]
			if get_inst_op_count(args) == 2:
				a = count_instruction_reg(self.rop_list, args)
				graph_binary_gadgets(a['Source'], a['Destination'], args + " usage")
			elif get_inst_op_count(args) == 1:
				print("Will implement a unary operation graph later.")
				a = count_instruction_reg(self.rop_list, args)
				graph_unary_gadgets(a, args + " Usage")

			elif get_inst_op_count(args) == 0:
				print("This instruction doesn't impact registers so it doesn't make sense to graph.")
				print(args + " appears " + str(count_instruction(self.rop_list, args)) + " times in the program.")
				print("==========")

			elif get_inst_op_count(args) == -1:
				print("That instruction isn't added to the counting function or is invalid.")
		else:
			print("Incorrect Number of Arguments!\nUsage 'instruction <inst_name>'")



class chain_menu(Cmd):
	def __init__(self, r):
		Cmd.__init__(self)
		self.rop_list = r

	def emptyline(self):
		pass

	def do_exit(self, args):
		return True

	def do_xor_swap(self, args):
		"""Create a chain to swap two registers using xor instructions."""
		valid_regs = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp']

		reg_1 = input("   Register 1-> ")
		reg_2 = input("   Register 2-> ")
		if reg_1 in valid_regs and reg_2 in valid_regs:
			xor_swap(self.rop_list, reg_1, reg_2)
		pass

	def do_move_constant(self, args):
		valid_regs = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp']
		target_register = input("   Target Register -> ")
		target_value = input("   Target Value -> 0x")
		target_value = int(target_value)

		hex_constant(self.rop_list,target_register, target_value)
			


