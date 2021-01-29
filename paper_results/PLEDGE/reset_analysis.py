import sys
import os

os.system("rm ./" + sys.argv[1] + "/experiment/oracle.csv")
os.system("rm ./" + sys.argv[1] + "/experiment/time_stat.csv")
os.system("rm ./" + sys.argv[1] + "/experiment/coverage.csv")
os.system("rm ./" + sys.argv[1] + "/experiment/coverage_limit.csv")

for i in range(10):
	os.system("rm ./" + sys.argv[1] + "/experiment/" + str(i) + "/analysis.csv")
	os.system("rm ./" + sys.argv[1] + "/experiment/" + str(i) + "/coverage_limit")
	os.system("rm ./" + sys.argv[1] + "/experiment/" + str(i) + "/coverage.csv")
	os.system("rm ./" + sys.argv[1] + "/experiment/" + str(i) + "/oracle")
	os.system("rm ./" + sys.argv[1] + "/experiment/" + str(i) + "/time_stat")




