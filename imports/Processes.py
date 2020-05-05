import psutil
import pefile
import re
import ropgadget
from terminaltables import AsciiTable
from os import system, chdir, getcwd, mkdir
import os.path


def find_process(pid):
	try:
		p = psutil.Process(pid)
		return p
	except Exception as e:
		print("The process cannot be accessed. Check your pid and try again.")
		return None

def get_mitigations(target):
	protections = {}

	try:
		dll = pefile.PE(target)

		protections['ASLR'] = dll.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE
		protections['DEP'] = dll.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NX_COMPAT
		protections['SafeSEH'] = dll.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NO_SEH
		protections['High_Entropy_VA'] = dll.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA
		protections['Base_address'] = hex(dll.OPTIONAL_HEADER.ImageBase)
		protections['Path'] = target
		return protections
	except Exception as e:
		# if an exception was raised for a module, just ignore it for now
		# print(target + " Wasn't found")
		return None


def get_process_mitigations(pid):
	p = find_process(pid)
	modules = {}

	if p is not None:
		print("Found " + str(len(p.memory_maps())) + " modules. Generating list of mitigations now.")

		c = 0
		for i in p.memory_maps(): # finds every import in memory
			if re.search('.exe$', i.path) is not None or re.search('.dll$', i.path) is not None:  # path must end with .dll or .exe
				mitigations = get_mitigations(i.path)
				c += 1
				if c % 10 == 0: # give an update every 10 modules to let people know the script is still working on larger apps
					print("Done with " + str(c) + " modules.")
				if mitigations is not None:
					name = i.path.split('\\') 
					name = name[len(name)-1]# get last part of path to get file name to use as dictionary keys
					modules[name] = mitigations
		# print(modules)
		return modules # returns nested dictionary with each module and it's mitigations

	else:
		return None


def create_mitigation_table(module_dict):
	if module_dict is not None:

		data_table = []

		table_header = ["Module Name", "ASLR", "DEP", "SafeSEH", "High_Entropy_VA", "Base_address"]
		data_table.append(table_header)

		for i in module_dict:
			row = []
			row.append(i)

			for p in range(1, len(table_header)):
				row.append(module_dict[i][table_header[p]])

			data_table.append(row)

		table = AsciiTable(data_table)

		print(table.table)

		return table


def create_gadget_file(mitigation_list):
	cmd = ""
	rop_path = ""
	system("cls")
	# table = create_mitigation_table(mitigation_list)
	working_list = mitigation_list.copy()
	all_modules = mitigation_list.copy()

	# cmd = input(" [->] ")

	while cmd != "generate":
		system("cls")
		table = create_mitigation_table(mitigation_list)

		print("=====Commands=====")
		print("- no-aslr")
		print("- no-dep")
		print("- no-safeSEH")
		print("- all - restore all of the modules")
		print("- generate - go to ROPfiles to make the lists")
		print("==================")

		cmd = input(" [->] ")
		cmd = cmd.lower()

		if cmd == "no-aslr":
			for m in mitigation_list.copy():
				if mitigation_list[m]['ASLR'] == True:
					working_list.pop(m)

		elif cmd == "no-dep":
			for m in mitigation_list.copy():
				if mitigation_list[m]['DEP'] == True:
					working_list.pop(m)

		elif cmd == "no-safeseh":
			for m in mitigation_list.copy():
				if mitigation_list[m]['SafeSEH'] == True:
					working_list.pop(m)

		elif cmd == "reset" or cmd == "all": # add all gadgets back
			mitigation_list = all_modules.copy()
			working_list = all_modules.copy()

		elif cmd == "generate":
			mods = []
			n = ""
			for i in working_list:
				mods.append(mitigation_list[i]['Path'])
				if i.find(".exe") >= 0:
					n = i

			if n == "":
				n = input("A good name wasn't found. Please provide one: ")


			p = getcwd()
			chdir(p + "\\Gadget_Sets")

			if os.path.isdir((n+ "_ROP")) == False:
				os.mkdir(n + "_ROP")
				os.chdir(n + "_ROP")
			else:
				os.chdir(n + "_ROP")

			print(getcwd())
			rop_path = ropgadget.main(mods, n, str(getcwd()))

		else:
			if cmd != "generate":
				print("Unknown command")

		mitigation_list = working_list.copy()
		system("cls")	
	return rop_path