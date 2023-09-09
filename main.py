from pprint import pprint
import re
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

## 1. Выполните пункты 1-3 задания.

PATTERN_PHONE = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
PHONE_SUB = r'+7(\2)-\3-\4-\5 \6\7'

# корректное заполнение Ф.И.О. и телефона по шаблону
def form(contact):
  if len(contact[0].split()) == 1 and len(contact[1].split()) == 1:
    return contact[0:5] + [re.sub(PATTERN_PHONE, PHONE_SUB, contact[5])] + contact[6:]
  elif len(contact[0].split()) == 2:
    x, y = contact[0].split()[0], contact[0].split()[1]
    return [x, y] + contact[2:5] + [re.sub(PATTERN_PHONE, PHONE_SUB, contact[5])] + contact[6:]
  elif len(contact[0].split()) == 3:
    x, y, z = contact[0].split()[0], contact[0].split()[1], contact[0].split()[2]
    return [x, y, z] + contact[3:5] + [re.sub(PATTERN_PHONE, PHONE_SUB, contact[5])] + contact[6:]
  elif len(contact[1].split()) == 2:
    x, y = contact[1].split()[0], contact[1].split()[1]
    return [contact[0]] + [x, y] + contact[3:5] + [re.sub(PATTERN_PHONE, PHONE_SUB, contact[5])] + contact[6:]  

# создание адресной книги 
phonebook = []
for data in contacts_list:
  correct_contacts_list = form(data)
  phonebook.append(correct_contacts_list)

# объединение всех дублирующиех записей о человеке в одну (по фамилии и имени)
def remove_duplicates(list):
    total_phonebook = []
    for contact_1 in phonebook:
        for contact_2 in phonebook:
            if contact_1[0:2] == contact_2[0:2]:
                new_contact = contact_1
                contact_1 = new_contact[0:2]
                for i in range(2, 7):
                    if new_contact[i] == '':
                        contact_1.append(contact_2[i])
                    else:
                        contact_1.append(new_contact[i])
        if contact_1 not in total_phonebook:
            total_phonebook.append(contact_1)

    return total_phonebook

total_phonebook = remove_duplicates(phonebook)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  
## Вместо contacts_list подставьте свой список:
  datawriter.writerows(total_phonebook)