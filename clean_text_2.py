import re

PUNCTION_PATTERN = r"(\;|\?|\:|\.+| -| –|\!)+\s*"

def main(f_in, f_out):
	# for line in f_in.readlines():
	line = next(f_in).replace("\n", '')
	i = 0

	while True:
		# print(line)
		m = re.search(PUNCTION_PATTERN, line)
		if m:
			# get first part and write to file
			out_line = line[:m.start()]
			f_out.write(out_line.strip() + '\n')
			# line is rest of line
			line = line[m.end():]
		else:
			# concatenate next line to current line
			try:
				next_line = next(f_in)
				next_line = re.sub(r"(,|“|”|‘|’|'|\")*", "", next_line).strip()


				line += ' ' + next_line
				line = line.replace('- ', '')
			except:
				pass

			if not line:
				break

		# if i == 10:
		# 	break
	
		i += 1
		

if __name__ == "__main__":
	file_in = open("datasets/de_aanslag_kort.txt", 'r')
	file_out = open('datasets/output.txt', 'w')
	main(file_in, file_out)

	file_in.close()
	file_out.close()