
my_int = 10
my_float = 10.5
my_str = "Python Programming"
my_list = [1, 2, 3, 4]
my_dict = {"name": "John", "age": 20}
my_set = {1, 2, 3}
my_tuple = (10, 20, 30)

print(my_int, type(my_int))
print(my_float, type(my_float))
print(my_str, type(my_str))
print(my_list, type(my_list))
print(my_dict, type(my_dict))
print(my_set, type(my_set))
print(my_tuple, type(my_tuple))

sales = [12000, 0, 8500, 15000, -200, 9800]

total = 0


for value in sales:
    
    if value <= 0:
        print("Skipped invalid value", value)
        continue

    
    total += value
    print("Added", value, "total", total)

    
    if total > 30000:
        break


if total > 30000:
    print("Target reached. Stopped at", total)
elif total == 30000:
    print("Target reached exactly")
else:
    print("Target not reached")