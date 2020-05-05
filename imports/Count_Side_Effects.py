from imports.Processes import *
from imports.Rop_File_Intake import *
from imports.Graphing_functions import *
from imports.ROP_Counting_Functions import *

import ropgadget
import os.path
from os import system, getcwd, chdir
import sys
import re

# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\EasyChat.exe_ROP\\EasyChat.exe_ROP_Gadgets.txt"
# gadgets = process_rop_file(f)


def get_ret_len(gadget):
	ret = gadget[(len(gadget) - 1)]
	ret = ret.split(" ")

	if len(ret) == 2:
		return 0
	elif len(ret) == 3:
		return int(ret[2], 16)
	else:
		print("Wh00ps!?")

def get_best_gadget(gadget_list, register, operation):
	operation = "pop"

	ret_len = 999999999
	best_len = 999999999	
	best_addy = 999999999
	best_gadget = ""

	for i in gadget_list:
		for inst in i['Gadget']:
			if inst.find(operation + " " + register) >= 0:
				if (len(i["Gadget"]) - 2) <= best_len and get_ret_len(i['Gadget']) <= ret_len:
					best_len = len(i["Gadget"]) - 2
					best_addy = i["Address"]
					ret_len = get_ret_len(i["Gadget"])
					best_gadget = i["Gadget"]
					break
			if best_len == 0 and ret_len == 0:
				break

	print(best_gadget)
	print("Address" + str(best_addy))
	print("Side effects in gadget: " + str(best_len))
	print("Return Length: " + str(ret_len))
	print("-------------------------------------------------------------------")



def get_best_gadget_binary(gadget_list, operation, source_reg, dest_reg=None):

	ret_len = 999999999
	best_len = 999999999	
	best_addy = 999999999
	best_gadget = ""

	if dest_reg == None:
		instruction = operation + " " + source_reg

	else:
		instruction = operation + " " + dest_reg + ", " + source_reg

	for i in gadget_list:
		for inst in i['Gadget']:
			if inst.find(instruction) >= 0:
				if (len(i["Gadget"]) - 2) <= best_len and get_ret_len(i['Gadget']) <= ret_len:
					best_len = len(i["Gadget"]) - 2
					best_addy = i["Address"]
					ret_len = get_ret_len(i["Gadget"])
					best_gadget = i["Gadget"]
					break
			if best_len == 0 and ret_len == 0:
				break

	if best_addy == 999999999:
		print("This instruction wasn't found in the set.")
	else:
		g = {}
		g['Address'] = best_addy
		g['SE_len'] = best_len
		g['Ret_len'] = ret_len
		g['Gadget'] = best_gadget

		return g
		print(best_gadget)
		print("Address" + str(best_addy))
		print("Side effects in gadget: " + str(best_len))
		print("Return Length: " + str(ret_len))
		print("-------------------------------------------------------------------")



def best_gadget_list(gadget_list, operation, dest_reg, source_reg=None):
	if source_reg == None: # unary instruction, ignore source reg
		instruction = operation + " " + dest_reg

	else: 
		instruction = operation + " " + dest_reg + ", " + source_reg

	g_list = []
	gad = {}

	for i in gadget_list:
		if i['Gadget'][0].find(instruction) >= 0:
			gad['SE_len'] = len(i["Gadget"]) - 2
			gad["Address"] = i["Address"]
			gad['Ret_len'] = get_ret_len(i["Gadget"])
			gad["Gadget"] = i["Gadget"]
			gad["Module"] = i['Module']
			g_list.append(gad)
			gad = {}

	 # returns list prioritizing least number of side effects then by length of return adjustment
	new_list = sorted(g_list, key=lambda k: k['Ret_len'])
	new_list = sorted(new_list, key=lambda j: j['SE_len'])

	if len(new_list) > 0:
		return new_list
	else:
		return 0

	# for i in new_list:
	# 	print(str(i['SE_len']) + " " + str(i['Ret_len']))
	# 	print(i['Gadget'])
	# 	print('---------------------------')


# test = best_gadget_list(gadgets, "inc", "ecx")

# if test != 0:
# 	for i in test:
# 		print(i)
# else:
# 	print("No Gadgets!")