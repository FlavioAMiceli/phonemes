import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

input_file = open('datasets/de_aanslag_kort.txt', 'r') 
input_lines = input_file.readlines()
output_file = open('datasets/output.txt', 'w')

def print_middle_line(result, line):
	left_out = ''
	if (line != ""):
		char_in_middle = re.search("\.|\;|\?", line)
	else:
		char_in_middle = re.search("\.|\;|\?", result)
	if (result != "" and result[len(result) - 1] == "-"):
		result = re.sub("-", "", result)
	if (line != "" and char_in_middle != None):
		result = result + " " + line[:char_in_middle.start() + 1]
	elif (line == "" and char_in_middle != None):
		left_out = result[char_in_middle.start() + 1:]
		result = result[:char_in_middle.start() + 1]
	print(bcolors.OKCYAN + "Writing Line : '" + bcolors.ENDC, result, "'")
	result.lstrip()
	output_file.write(result)
	output_file.write("\n")
	if (line != "" and char_in_middle != None):
		result = line[char_in_middle.start() + 1:]
	elif (line == "" and char_in_middle != None):
		result = left_out
	result = result.lstrip()
	print(bcolors.OKCYAN + "Left in result : '" + bcolors.ENDC, result, "'")
	return result

count = 0
result = ""
for line in input_lines:
	count += 1
	# if count == 114:
	# 	exit()
	print("\n===============================================================")
	print(bcolors.HEADER + "\nOriginal Line ", count, "\n" + bcolors.ENDC, line)
	line = line.strip('\n')
	line = re.sub("‘|’", "", line)
	dot_at_end = re.search('[.]$', line)
	dash_at_end = re.search('[-]$', line)
	end_char_in_middle = re.search("\.|\;|\?", line)
	if (end_char_in_middle != None and dot_at_end == None):
		print(bcolors.OKGREEN + "Writing Middle Line in File" + bcolors.ENDC)
		result = print_middle_line(result, line)
	elif (dot_at_end != None and result == ""):
		print(bcolors.OKGREEN + "Printing Line Ready" + bcolors.ENDC)
		print(line)
		output_file.write(line)
		output_file.write("\n")
	elif (dot_at_end != None and result != ""):
		result = result + line
		print(bcolors.OKGREEN + "Writing Result in File" + bcolors.ENDC)
		print(result)
		output_file.write(result)
		output_file.write("\n")
		result = ""
	else:
		print(bcolors.FAIL + "Not Printing - Adding in result" + bcolors.ENDC)
		line = line.rstrip()
		if (result != "" and result[len(result) - 1] == "-"):
			result = re.sub("-", "", result)
			result = result + line
		else:
			result = result + " " + line
		result = result.lstrip()
		print(bcolors.OKCYAN + "New Result : '" + bcolors.ENDC, result, "'")
	end_char_in_middle = re.search("\.|\;|\?", result)
	if (end_char_in_middle != None and dot_at_end == None):
		print(bcolors.BOLD + "Writing Middle RESULT in File" + bcolors.ENDC)
		result = print_middle_line(result, "")

input_file.close()
output_file.close()