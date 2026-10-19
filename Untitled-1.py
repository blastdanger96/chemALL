#num = int(input("Nigga type"))

#for i in range (1, num+1):
#        print(1, end="\t")
l = int(input("Enter the lower limit:"))
num = int(input("Enter the upper limit:"))
for i in range (l, num+1):
    for j in range (1,11):
        print(i*j)
    print(end='\t')