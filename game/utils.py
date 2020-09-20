import numpy as np

def sh_d_one(arr, wd, idx):
	for i in range(idx, 0, -1):
		arr[i] = arr[i-1]
	for j in range(wd):
		arr[0,j] = 0