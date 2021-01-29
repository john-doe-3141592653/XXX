import sys, os

for i in range(10):
	valid = []
	with open("./experiment/" + str(i) + "/oracle", "r") as f:
		index = 0
		for line in f:
			print(index)
			if line.replace("\n", "") == "False":
				valid.append(index)
			index += 1
	print(str(i) + " -> " + str(valid))
	names = os.listdir("./gnf")
	next_folder = len(names) - 1

	for v in valid:
		os.system("mkdir ./gnf/test_case_" + str(next_folder))
		os.system("cp -r ./experiment/" + str(i) + "/test_case_" + str(v) + "/* ./gnf/test_case_" + str(next_folder))
		next_folder += 1
