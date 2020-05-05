from imports.Processes import *
from imports.Rop_File_Intake import *
from imports.Graphing_functions import *
from imports.ROP_Counting_Functions import *
from imports.Count_Side_Effects import *
from imports.Chain_Generator import *
from imports.SubMenus import *

import ropgadget
import os.path
from os import system, getcwd, chdir
import sys

def program_start():
	if len(sys.argv) == 1: # no added arguments
		a = input("Do you have a file generated already? (y or n): ")

		if a.lower() == 'y': # load file and go to main menu
			rop_file = input("Enter rop file path: ")

			if os.path.exists(rop_file):
				gadget_list = process_rop_file(rop_file)
				return gadget_list
			else:
				print("Check your file and come back later")
				exit()

		else:
			a = input("Process or executable file? (process or exe): ")
			if a == "process": # use functions to get mitigations, filter module, pass paths into ROPgadget
				mitigation_list = ""
				rop_file = ""

				pid = input("Enter PID: ")
				mitigation_list = get_process_mitigations(int(pid))
				rop_file = create_gadget_file(mitigation_list) # ask which modules to use, pass to ROPGadget

				gadget_list = process_rop_file(rop_file)
				return gadget_list

			elif a == "exe": # Pass path into ROPgadget
				exe_path = input("Path--->")
				print(os.path.exists(exe_path))
				n = input("Name")
				n = n.replace(' ', '_')
				rop_path = ropgadget.main([exe_path], n, str(getcwd()))
				exit()
				pass


	elif len(sys.argv) == 2: # one argument (for file path)
		print(">")
		exit()

	else:
		print("Usage: 'Main.py pid=1234' or Main.py <executable path> ")
		exit()


def select_menu(rop_list):
	system("cls")

	menus = ['Graphing', "Search", "Chains"]

	# print("Menu Select: ")
	for m in menus:
		print("-" + m)
		pass

	selection = ""

	while selection != "exit":
		if selection == "graphing":
			g_menu = graphing_menu(rop_list)
			g_menu.prompt = "\n[Graphs->]"
			g_menu.cmdloop("Starting Graph Menu")

		elif selection == "search":
			print("This feature not yet implemented")
			pass
		elif selection == "chains":
			c_menu = chain_menu(rop_list)
			c_menu.prompt = "[Chains->]"
			c_menu.cmdloop("Starting Chains")


		# elif selection == "test":
		# 	print(len(rop_list))
		# 	print(rop_list[1232])
		# 	print(getcwd())
		else:
			print("Command not found.")

		selection = input("-> ")
		selection = selection.lower()

#--------------#
# --- MAIN --- #
#--------------#

gadgets = program_start() # asks about how gadget file will be loaded, creates dictionay for each gadget
select_menu(gadgets)
