a =("0:0-0:5, 0:35-0:40")

split=a.split(',')

# print(split)


cuts=[]
for i,j in enumerate(split):
    # print(i,j)
    temp = tuple(j.split('-'))
    # print(temp)
    cuts.append(temp)
    
# print(cuts)




