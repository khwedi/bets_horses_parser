# string = 'Gun Pilot'
#
# new = string.split()
# new2 = '+'.join(new)
# print(new2)

# test = {'apple':'fruit', 'banana': 'yellow', 'banana': 'green'}
#
# print(test.keys())
#
# for i in test.keys():
#     if i == 'apple':
#         test[i] = 'no'
# print(test)
# my_dict = {}
# test = ['apple', 'banana', 'banana']
#
# # Добавление ключей и пустых списков
# for key in test:
#     if key not in my_dict:  # Проверка, существует ли ключ
#         my_dict[key] = []   # Присваиваем пустой список только если ключ ещё не добавлен
#
# my_dict['banana'].append('y')
# my_dict['banana'].append('х')
# # Вывод результата
# print(my_dict)
# a = []
# for i in my_dict:
#     for j in my_dict[i]:
#         j = j+'g'
#         a.append(j)
# print(a)


# date1 = '2024-11-03 01:49:33'
# date2 = '2024-11-03 02:00:33'
#
# zabeg1 = '2024-11-03 02:05:33'
# zabeg2 = '2024-11-03 03:05:33'


elements = [1,2,3,4,5,6,7,8,9,10]
batch_size = 2

for i in range(0, len(elements), batch_size):
    batch = elements[i:i + batch_size]
    print(f"Batch {i // batch_size + 1}: {batch}")


