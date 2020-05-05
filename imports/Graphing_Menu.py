class graph_menu(Cmd):
	# returns multiple arguments as a list, changes any strings that are ints to type int
	def process_multi_args(self, args):
		args = args.split()    
		for i, arg in enumerate(args):
			if arg.isdigit():
				args[i] = int(args[i])
		return args

	def emptyline(self):
		pass

	def do_exit(self, args):
		print("-===Returning to Main Menu===-\n")
		return True
	def do_quit(self, args):
		print("-===Returning to Main Menu===-\n")
		return True

	def do_registers(self,args):
		"""Graph all occurances of all registers.(Takes no arguments)"""
		a = count_register_use(main_menu.rop_gadgets)
		graph_registers(a, "All Register Use")

	def do_instruction(self,args):
		"""Graph all occurances of an instruction."""
		args = self.process_multi_args(args)

		if len(args) == 1:
			args = args[0]
			if get_inst_op_count(args) == 2:
				a = count_instruction_reg(main_menu.rop_gadgets, args)
				graph_binary_gadgets(a['Source'], a['Destination'], args + " usage")
			elif get_inst_op_count(args) == 1:
				print("Will implement a unary operation graph later.")
				a = count_instruction_reg(main_menu.rop_gadgets, args)
				graph_unary_gadgets(a, args + " Usage")

			elif get_inst_op_count(args) == 0:
				print("This instruction doesn't impact registers so it doesn't make sense to graph.")
				print(args + " appears " + str(count_instruction(main_menu.rop_gadgets, args)) + " times in the program.")
				print("==========")

			elif get_inst_op_count(args) == -1:
				print("That instruction isn't added to the counting function or is invalid.")
		else:
			print("Incorrect Number of Arguments!\n")

