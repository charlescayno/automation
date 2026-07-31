dim_list = [1,3,4,10]


for i in range(len(dim_list)):
    for dim in dim_list:
        if dim_list[i] < dim:
            start = dim_list[i]
            end = dim
            print(f"{start}-{end}")

for i in range(len(dim_list)):
    for dim in dim_list:
        if dim_list[i] > dim:
            start = dim_list[i]
            end = dim
            print(f"{start}-{end}")

