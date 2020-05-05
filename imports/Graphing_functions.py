import matplotlib.pyplot as plt
import numpy as np
import collections
# from ROP_Counting_Functions import count_register_use, prepare_gadgets, count_derefrenced_registers, count_instruction_reg
# import ROP_Counting_Functions
# --------------------
# ---setup graphing---
# --------------------
import os

def graph_registers(gadget_list, title):
	x = []

	for i in gadget_list.keys():
		x.append(i) 

	objects = x
	y_pos = np.arange(len(objects))
	performance = gadget_list.values()

	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Times Used')
	plt.title(title)

	# add labels to height of bars
	for i,v in enumerate(performance):
		plt.text(i-0.2, v+0.1, str(v))


	plt.show()


def graph_binary_gadgets(source_dict, dest_dict, title):

	labels = source_dict.keys()
	x = np.arange(len(labels))
	width = 0.35

	fig, ax = plt.subplots()
	rects2 = ax.bar(x - width/2, dest_dict.values(), width, label='Destination')
	rects1 = ax.bar(x + width/2, source_dict.values(), width, label='Source')

	ax.set_ylabel('Count')
	ax.set_title(title)
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()

	for i in rects1:
		height = i.get_height()
		ax.annotate('{}'.format(height),
                    xy=(i.get_x() + i.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

	for i in rects2:
		height = i.get_height()
		ax.annotate('{}'.format(height),
                    xy=(i.get_x() + i.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
	fig.autofmt_xdate()
	fig.tight_layout()

	plt.show()


def graph_unary_gadgets(gadget_dict, title):

	labels = gadget_dict.keys()
	x = np.arange(len(labels))
	width = 0.35

	fig, ax = plt.subplots()
	rects = ax.bar(x + width/2, gadget_dict.values(), width, label='Source')

	ax.set_ylabel('Count')
	ax.set_title(title)
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()

	for i in rects:
		height = i.get_height()
		ax.annotate('{}'.format(height),
                    xy=(i.get_x() + i.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

	fig.autofmt_xdate()
	fig.tight_layout()
	plt.show()


# def graph_binary_op(gadget_list, title):
# 	objects = gadget_list.keys()
# 	y_pos 


# -----------------
# ---Process Rop---
# -----------------

# gad_list = ROP_Counting_Functions.prepare_gadgets("C:\\Users\\User\\Desktop\\Rop_testing\\Gadget_sets\\media_monkey_decoder.txt")

# # a = count_register_use(gad_list)
# # b = count_derefrenced_registers(gad_list, 's')
# # c = count_derefrenced_registers(gad_list, 'd')
# d = count_instruction_reg(gad_list, 'pop')
# print(d)

# insts = ['pop', 'push', 'call', 'inc', 'dec', 'idiv']

# for i in insts:
# 	a = count_instruction_reg(gad_list, i)
# 	graph_gadgets(a, 'Usage of "' + i + '" instruction')

# graph_binary_gadgets()