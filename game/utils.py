import numpy as np

def sh_d_one(arr, ht, wd):
	for i in range(ht-1, 0, -1):
		arr[i] = arr[i-1]
	for j in range(wd):
		arr[0,j] = 0