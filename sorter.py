"""
Задание # 2:
Напишите программу, которая в указанной пользователем директории найдет все файлы указанного пользователем формата
и перенесет их в указанную пользователем директорию.
"""
import os

# user inputs
# directory = r"C:\Users\Perkyssia\PycharmProjects\my_it_school\venv\back\practice"
directory = input(r"Введите директорию в которой хотите произвести поиск файлов по их формату: ")

files_format = input("Введите формат файлов для поиска: ")

# remove_directory = directory + r"\archives" # тестил на rar и zip архивах
# C:\Users\Perkyssia\PycharmProjects\my_it_school\venv\back\practice\archives
remove_directory = input(r"Введите конечную директорию сохранения файлов: ")

new_directory_choice = input("Нужно ли создать новую директорию "
                             "в конечной директории? 1 - да, Enter - нет: "
                             )

# go to dir from user input
os.chdir(directory)

# add new directory
if new_directory_choice == "1":
    new_directory = input("Введите название новой директории(без символов <, >, :, \", \\, /, |): ")
    os.chdir(new_directory)
    try:
        os.mkdir(new_directory)
    except OSError:
        print("Директория archives уже существует")
        pass

# all files in directory
files = os.listdir(directory)

# move all files to new directory
for i in files:
    if i.endswith(files_format):
        if os.path.isfile(remove_directory + f"\\{i}"):
            os.rename(directory + f"\\{i}", remove_directory + f"\\renamed_{i}")
            print(f"Файл {i} переименован в renamed_{i}, "
                  f"т.к. файл с таким именем уже существовал в конечной директории")
        else:
            os.replace(directory + f"\\{i}", remove_directory + f"\\{i}")

print("Выполнение программы завершено")