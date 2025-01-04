import os
import csv
import re
import logging
from logging.handlers import RotatingFileHandler

# Создание необходимых папок
log_dir = 'logs'

# Проверяем и создаем директории, если они не существуют
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования с ротацией
log_file = os.path.join(log_dir, 'contacts.log')
logger = logging.getLogger('ContactsLogger')
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


try:
    with open("data.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    logger.info("Данные успешно прочитаны из файла data.csv")
except Exception as e:
    logger.error(f"Ошибка при чтении файла: {e}")


def normalize_phone(phone):
    phone = re.sub(r'[- () доб.]', '', phone)  
    if phone.startswith('8'):
        phone = '+7' + phone[1:]  
    elif phone.startswith('7'):
        phone = '+' + phone  
    
   
    if len(phone) == 12 and phone.startswith('+7'):
        return f'+7 ({phone[2:5]}) {phone[5:8]}-{phone[8:10]}-{phone[10:]}'
    
    elif len(phone) > 13:  
        main_number = phone[:-4]  
        ext_number = phone[-4:]    
        if len(main_number) == 12 and phone.startswith('+7'):
            return f'+7 ({main_number[2:5]}) {main_number[5:8]}-{main_number[8:10]}-{main_number[10:]} доб.{ext_number}'

    elif len(phone) > 11 and not phone.startswith('+7') and not phone.startswith('7'):  
             main_number = phone[-10:]
             country_code = phone[:-10]
             return f'{country_code} ({main_number[0:3]}) {main_number[3:6]}-{main_number[6:8]}-{main_number[8:]}'

    return phone  


normalized_contacts = {}
for contact in contacts_list:
    fio_parts = " ".join(contact[:3]).split()
    lastname = fio_parts[0] if len(fio_parts) > 0 else ''
    firstname = fio_parts[1] if len(fio_parts) > 1 else ''
    surname = fio_parts[2] if len(fio_parts) > 2 else ''
    
    
    phone = normalize_phone(contact[5]) if len(contact) > 5 else ''
    
    
    email = contact[6] if len(contact) > 6 else ''

    
    key = (lastname, firstname)
    if key not in normalized_contacts:
        normalized_contacts[key] = [lastname, firstname, surname, contact[3], contact[4], phone, email]
        logger.info(f"Добавлен новый контакт: {lastname} {firstname}")
    else:
        existing_contact = normalized_contacts[key]
        if existing_contact[3] != contact[3]:
            existing_contact[3] += f"; {contact[3]}"
        if existing_contact[4] != contact[4]:
            existing_contact[4] += f"; {contact[4]}"
        if existing_contact[5] != phone and phone:
            existing_contact[5] = phone
        if existing_contact[6] != email and email:
            existing_contact[6] += f"; {email}"
        logger.info(f"Обновлен контакт: {lastname} {firstname}")


final_contacts_list = [list(key) + value[2:] for key, value in normalized_contacts.items()]


try:
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_contacts_list)
    logger.info("Данные успешно сохранены в файл phonebook.csv")
except Exception as e:
    logger.error(f"Ошибка при записи в файл phonebook.csv: {e}")

column_widths = [max(len(str(item)) for item in column) for column in zip(*final_contacts_list)]


def format_row(row):
    return " | ".join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row))


try:
    with open('contacts.txt', 'w', encoding='utf-8') as file:
        
        file.write(format_row(final_contacts_list[0]) + '\n')
        file.write("-" * (sum(column_widths) + len(column_widths) * 3 - 1) + '\n')  # Разделитель
        
        
        for row in final_contacts_list[1:]:
            file.write(format_row(row) + '\n')
    logger.info("Данные успешно сохранены в файл contacts.txt")
except Exception as e:
    logger.error(f"Ошибка при записи в файл contacts.txt: {e}")

print("Данные успешно сохранены в файл contacts.txt")
