import os
import json
from pathlib import Path
from sys import platform
import time
import tkinter
from tkinter import *
from tkinter import messagebox

import yaml
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import SearchPage
from logging_dir.logging import my_exception_hook, set_logger
from main import fill_advanced_search_settings_page, unpack_info_file, unpack_dict, send_cookies, check_authorization, \
    check_element_exist, send_responses_on_page, click, logging_final_results, check_driver_exist

# TODO: encoding yaml need to fix
# TODO: че делать с хромдрайвером для винды и линукса?
# TODO: логгирование в окошки уведомлений превратить
# TODO: еще раз поглядеть, как выглядит структуризация функций в тестировании и назначение драйвера
# TODO: растянуть поле ввода сопроводительного вширь 
# TODO: переделать дизайн, нормально прошарив grid и остальные две штуки
# TODO: почему драйвер не присваивается в scope функции?
# TODO: придумать, каким образом присвоить драйвер. Для этого нужно как минимум вывести его из скоупа функции. Для этого нужно научиться получать значения из input
# TODO: кнопка "остановить процесс"


class AddElement():
    def __init__(self):
        elem_count = 0
        self.elem_count = elem_count

    def counting(self):
        self.elem_count += 1

    # TODO: таки приделать декоратор
    # @counting()
    def create_default_label(self, text, pady=0, font_size=16, font_family='PT Sans', thickness='normal'):
        self.label = Label(frame, text=text, bg='#F3F5F4', justify='left')
        self.label.config(font=(font_family, font_size, thickness))
        self.label.grid(sticky=W, column=0, row=self.elem_count, pady=pady)
        self.counting()

    def create_input(self, text):
        string_for_input = StringVar(frame, text)
        self.input = Entry(frame, highlightthickness=1, bg='white', width=40, textvariable=string_for_input,
                           font=('Helvetica', 10))
        self.input.grid(sticky=W, column=0, row=self.elem_count)
        self.counting()
        return self.input

    def create_radio(self, button, tuple, number_of_set_items, font_family='Helvetica', font_size=14,
                     font_thickness='normal'):
        button.set(number_of_set_items)

        for text, value in tuple:
            radio = Radiobutton(frame, text=text, variable=button, bg='#F3F5F4', highlightthickness=0,
                                value=value,
                                justify='left')
            radio.config(font=(font_family, font_size, font_thickness))
            radio.grid(sticky=W, column=0, row=self.elem_count)
            self.counting()


def create_label(text, row, *kwargs):
    label = Label(frame, text=text, bg='#F3F5F4', justify='left')
    label.config(font=('PT Sans', 16, kwargs))
    label.grid(sticky=W, column=0, row=row)


def dump_cookies(driver, fp):
    cookies = driver.get_cookies()
    # TODO: создать переменную с куки-файлом
    # TODO: проверку авторизации сделать
    with open(fp, 'w') as cookie_file:
        json.dump(cookies, cookie_file, indent=6)


def check_cookie_exist(fp):
    if os.path.isfile(fp) and os.path.getsize(fp):
        return True
    else:
        return False


def dump_in_my_file(info, fp):
    with open(fp, 'w', encoding='utf8') as file:
        yaml.dump(info, file, allow_unicode=True, encoding=None)


def raise_error_about_authorization():
    message = 'Сейчас вам необходимо авторизироваться. Эту процедуру нужно пройти один раз. В будущем авторизация будет проходить автоматически. Как только залогинитесь, нажмите "ok"'
    messagebox.showinfo(title='Введите данные на странице HH', message=message)
    root.update()


# def new_func_for_btn(input_data):
#     print('Введите свои данные!!!')
#     search_key_from_input = searchKeyInput.get()
#     region_from_input = regionInput.get()
#     resume_name_from_input = resumeNameInput.get()
#
#     search_period_from_input = r_search_period.get()
#     items_on_page_from_input = r_items_on_page.get()
#     order_from_input = r_order.get()
#     input_data['search_key'] = search_key_from_input
#     input_data['resume_name'] = resume_name_from_input
#     input_data['region'] = region_from_input
#     input_data['search_period'] = search_period_from_input
#     input_data['items_on_page'] = items_on_page_from_input
#     input_data['order'] = order_from_input
#     input_data['about_mailing'] = {'last_block_time': last_block_time_from_file,
#                                    'count_of_responses': count_of_responses_from_file, 'time': time_from_file}

def btn_click():
    error_message = 'В корневой папке не найдет ChromeDriver!\n' \
                    'Если у вас Windows, файл хромдрайвера должен называться: "chromedriver.exe"\n' \
                    'Если у вас Linux, файл хромдрайвера должена называться: "chromedriver"\n' \
                    'О том, как установить chomedriver можно прочесть в README-файле проекта'

    if platform == 'linux' or platform == 'linux2':
        driver_path = DRIVER_PATH_LINUX
    elif platform == 'win32':
        driver_path = 'chromedriver.exe'
    else:
        messagebox.showerror(title='Система не определена', message='У вас винда или линукс?')
        sys.exit()

    if not check_driver_exist(driver_path):
        # TODO: добавить в readme инструкцию по установке хромдрайвера

        messagebox.showerror(title='Хромдрайвера нет в папке', message=error_message)
        raise FileNotFoundError

    search_key_from_input = searchKeyInput.get()
    region_from_input = regionInput.get()
    resume_name_from_input = resumeNameInput.get()
    covering_letter_from_input = coveringLetterInput.get()

    search_period_from_input = r_search_period.get()
    items_on_page_from_input = r_items_on_page.get()
    order_from_input = r_order.get()

    info_str = f'Ключевые слова: {str(search_key_from_input)}\n' \
               f'Название вашего резюме: {str(resume_name_from_input)}\n' \
               f'Регион: {str(region_from_input)}\n' \
               f'Сортировка: {str(search_period_from_input)}\n' \
               f'Выводить: {str(order_from_input)}\n' \
               f'Показывать на странице: {str(items_on_page_from_input)}\n'
    messagebox.showinfo(title='Проверьте информацию!', message=info_str)
    root.update()

    # if os.path.isfile(INFO_FILE) and os.path.getsize(INFO_FILE) and check_if_info_been_changed(search_key_from_input,
    #                                                                                            region_from_input,
    #                                                                                            search_period_from_input,
    #                                                                                            items_on_page_from_input,
    #                                                                                            order_from_input):
    input_dict = {
        'search_key': search_key_from_input,
        'resume_name': resume_name_from_input,
        'region': region_from_input,
        'search_period': search_period_from_input,
        'items_on_page': items_on_page_from_input,
        'order': order_from_input,
        'covering_letter': covering_letter_from_input,
    }

    dump_in_my_file(input_dict, INFO_FILE)

    driver = webdriver.Chrome(Path(driver_path).resolve())

    driver.get(AUTHORIZATION_PAGE_LINK)

    if not check_cookie_exist(COOKIES_FILE):
        raise_error_about_authorization()

        dump_cookies(driver, COOKIES_FILE)

    driver = send_cookies(driver, COOKIES_FILE)
    driver.get(AUTHORIZATION_PAGE_LINK)

    if not check_authorization(driver):
        while not check_authorization(driver):
            message = 'Вы не авторизованы. Ничего страшного. Авторизуйтесь и в следующий раз вам не придется этого делать. После авторизации нажмите "ок" в этом окне'
            messagebox.showerror(title='Траблы с атворизацией', message=message)
            root.update()
            driver.get(AUTHORIZATION_PAGE_LINK)

    else:
        logger.info('Авторизация прошла успешно')
    fill_advanced_search_settings_page(driver, search_key_from_input, region_from_input, search_period_from_input,
                                       items_on_page_from_input,
                                       order_from_input)  # messagebox.showerror(title='', message='Error always')

    number_of_responses = 0
    number_of_pages = 1

    # TODO: функция, которая берет общее количество страниц. В пизду пока. Если страниц меньше 6, кнопки с финальной страницей нет.
    # TODO: Настроить рассылку по заданному количеству откликов
    if check_element_exist(driver, SearchPage.next_page_button):
        while WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, SearchPage.next_page_button))):
            # тут должно располагаться все
            logger.debug(f'Перешли на страницу: {number_of_pages}')

            number_of_pages += 1
            send_responses_on_page(driver, resume_name_from_input, INFO_FILE, covering_letter_from_input,
                                   number_of_responses, number_of_pages)

            click(driver, SearchPage.next_page_button)

    else:
        logger.info('Страница всего одна!')
        send_responses_on_page(driver, resume_name_from_input, INFO_FILE, covering_letter_from_input,
                               number_of_responses, number_of_pages)

    time.sleep(4)
    logging_final_results(number_of_responses, number_of_pages)


sys.excepthook = my_exception_hook
set_logger()

dict_from_input = {}

INFO_FILE = 'my_info.yml'
COOKIES_FILE = 'cookies.json'
DRIVER_PATH_WINDOWS = 'chromedriver.exe'
DRIVER_PATH_LINUX = 'chromedriver'
AUTHORIZATION_PAGE_LINK = 'https://spb.hh.ru/account/login?backurl=%2F'

if os.path.isfile(INFO_FILE) and os.path.getsize(INFO_FILE):
    info_file_dict = unpack_info_file(INFO_FILE)
    search_key_from_file, resume_name_from_file, region_from_file, search_period_from_file, items_on_page_from_file, order_from_file, covering_letter_from_file = unpack_dict(
        info_file_dict)

else:
    search_key_from_file = ''
    resume_name_from_file = ''
    region_from_file = ''
    covering_letter_from_file = ''

    search_period_from_file = 0
    order_from_file = 'publication_time'
    items_on_page_from_file = 100

root = tkinter.Tk()

root.option_add('*Dialog.msg.font', 'Helvetica 12')

root['bg'] = '#F3F5F4'
root.title('Рассылка HH-откликов')
# Прозрачность окна
root.wm_attributes('-alpha', 1)
root.geometry('300x851')
root.resizable(width=True, height=True)

# холст для вывода графич. примитивов. Не явл. обязательным
# canvas = Canvas(root, height=300, width=250).pack()

# рамка, содержащая другие графич. компоненты
frame = Frame(root, bg='#F3F5F4')
# relwidth=1, relheight=1 на всю ширину и высоту, relx и rely - смещение. Все это в процентах
frame.place(relwidth=1, relheight=1, relx=0.10, rely=0.05)

a = AddElement()
create_label('Ключевые слова', 1)

a.create_default_label('Введите свои данные', font_size=28, thickness='bold')

a.create_default_label('Ключевые слова')
searchKeyInput = a.create_input(search_key_from_file)

a.create_default_label('Название вашего резюме')

resumeNameInput = a.create_input(resume_name_from_file)

a.create_default_label('Регион')

regionInput = a.create_input(region_from_file)

a.create_default_label('Введите сопроводительное письмо')

coveringLetterInput = a.create_input(covering_letter_from_file)

a.create_default_label('Сортировка')

ORDER = [
    ('По дате изменения', 'publication_time'),
    ('По убыванию зарплат', 'salary_desc'),
    ('По возрастанию зарплаты', 'salary_inc'),
    ('По соответствию', 'relevance'),
]

r_order = StringVar()

a.create_radio(r_order, ORDER, order_from_file)

a.create_default_label('Выводить')

SEARCH_PERIOD = [
    ('За всё  время', 0),
    ('За месяц', 30),
    ('За неделю', 7),
    ('За последние три дня', 3),
    ('За сутки', 1),
]

r_search_period = IntVar()

a.create_radio(r_search_period, SEARCH_PERIOD, search_period_from_file)

a.create_default_label('Показать на странице')

ITEMS_ON_PAGE = [
    ('20 вакансий', 20),
    ('50 вакансий', 50),
    ('100 вакансий', 100),
]

r_items_on_page = IntVar()

a.create_radio(r_items_on_page, ITEMS_ON_PAGE, items_on_page_from_file)

btn = Button(frame, text='Начать рассылку', bg='#F7C87E', command=btn_click, justify=LEFT,
             border=0)
btn.config(height=2, width=15)
btn.grid(sticky=W, column=0, row=24, pady=28)

root.mainloop()
