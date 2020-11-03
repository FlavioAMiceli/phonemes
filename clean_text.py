import re

# Colors used for debugging purposes
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

# The characters we accept as ending characters are the following :
# '.' followed by anything but a dot
# ';'
# '?'
# ':'
# When we find one of these characters we will split the line 
# and accept it as a complete sentence
pattern = "\.(?:[^\.])|\;|\?|\:"

# Function that is called when we have a complete sentence and we write it
# in the output file
def write_line_in_file(result):
	result.lstrip()
	print(bcolors.OKCYAN + "Writing Line in File : '" + bcolors.ENDC, result, "'")
	output_file.write(result)
	output_file.write("\n")

# Function that is called when we find a terminating character
# in the middle of the line
def print_middle_line(result, line):
	left_out = ''
	if (line != ""):
		char_in_middle = re.search(pattern, line)
	else:
		char_in_middle = re.search(pattern, result)
	if (result != "" and result[len(result) - 1] == "-"):
		result = re.sub("-", "", result)
	if (line != "" and char_in_middle != None):
		if result != "":
			result = result + " " + line[:char_in_middle.start() + 1]
		else:
			result = line[:char_in_middle.start() + 1]
	elif (line == "" and char_in_middle != None):
		left_out = result[char_in_middle.start() + 1:]
		result = result[:char_in_middle.start() + 1]
	write_line_in_file(result)
	if (line != "" and char_in_middle != None):
		result = (line[char_in_middle.start() + 1:]).lstrip()
	elif (line == "" and char_in_middle != None):
		result = left_out.lstrip()
	print(bcolors.OKCYAN + "Result (left):'" + bcolors.ENDC, result, "'")
	return result

# Function that is called to check the different cases to split a line
def check_cases(line, result):
	dot_at_end = re.search('[.]$', line)
	dash_at_end = re.search('[-]$', line)
	end_char_in_middle = re.search(pattern, line)
	if (end_char_in_middle != None and dot_at_end == None):
		print(bcolors.OKGREEN + "Found ending character in the middle of line" + bcolors.ENDC)
		result = print_middle_line(result, line)
	elif (dot_at_end != None and result == ""):
		print(bcolors.OKGREEN + "Line Ready" + bcolors.ENDC)
		write_line_in_file(line)
	elif (dot_at_end != None and result != ""):
		result = result + line
		print(bcolors.OKGREEN + "Result in File" + bcolors.ENDC)
		write_line_in_file(result)
		result = ""
	else:
		print(bcolors.FAIL + "Not Printing - Adding in result" + bcolors.ENDC)
		# line = line.rstrip()
		if (result != "" and result[len(result) - 1] == "-"):
			result = re.sub("-", "", result)
			result = result + line
		else:
			result = result + " " + line
		result = result.lstrip()
		print(bcolors.OKCYAN + "Result:'" + bcolors.ENDC, result, "'")
	end_char_in_middle = re.search(pattern, result)
	if (end_char_in_middle != None and dot_at_end == None):
		print(bcolors.BOLD + "Middle RESULT in File" + bcolors.ENDC)
		result = print_middle_line(result, "")
	return result

def clean_text(file_to_clean):
	input_file = open(file_to_clean, 'r') 
	input_lines = input_file.readlines()
	count = 0
	result = ""
	# Main for loop that iterates through each of the lines of the input file
	# and splits them (or not) according the terminating character it finds (or not)
	for line in input_lines:
		count += 1
		print("\n===============================================================")
		print(bcolors.HEADER + "Original Line ", count, "\n'", line, "'" + bcolors.ENDC)
		line = line.strip('\n')
		line = re.sub("‘|’", "", line)
		result = check_cases(line, result)
	input_file.close()
	output_file.close()

if __name__ == "__main__":
	file_to_clean = "datasets/de_aanslag_kort.txt"
	output_file = open('datasets/output.txt', 'w')
	clean_text(file_to_clean)