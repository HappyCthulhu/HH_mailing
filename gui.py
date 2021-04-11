import os
import json
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
    check_element_exist, send_responses_on_page, click, logging_final_results


# TODO: че делать с хромдрайвером для винды и линукса?
# TODO: логгирование в окошки уведомлений превратить
# TODO: еще раз поглядеть, как выглядит структуризация функций в тестировании и назначение драйвера
# TODO: растянуть поле ввода сопроводительного вширь 
# TODO: переделать дизайн, нормально прошарив grid и остальные две штуки
## работа с классами в Tkinter
## каким образом назначать порядок для grid?
# TODO: почему драйвер не присваивается в scope функции?
# TODO: придумать, каким образом присвоить драйвер. Для этого нужно как минимум вывести его из скоупа функции. Для этого нужно научиться получать значения из input
# TODO: может стоит сделать отдельный файл для 'about_mailing'? А то передавать их аргументы каждый раз нет смысла
# TODO: рассылка вакансий
# TODO: кнопка "остановить процесс"

class AddElement():
    def
    def create_label(self, text):
        self.label = Label(frame, text=text, bg='#F3F5F4', justify='left')
        self.label.config(font=('PT Sans', 16, kwargs))
        self.label.grid(sticky=W, column=0, row=row)

def create_input(text):
    test_var = StringVar(frame, text)
    input_ = Entry(frame, highlightthickness=1, bg='white', width=40, textvariable=test_var,
                   font=('Helvetica', 10))
    return input_
    # searchKeyInput.pack(pady=18)


def create_radio(tuple, variable):
    for text, value, row_count in tuple:
        radio = Radiobutton(frame, text=text, variable=variable, bg='#F3F5F4', highlightthickness=0, value=value,
                            justify='left')
        radio.config(font=('Helvetica', 14, 'normal'))
        radio.grid(sticky=W, column=0, row=row_count)


def create_label(text, row, *kwargs):
    label = Label(frame, text=text, bg='#F3F5F4', justify='left')
    label.config(font=('PT Sans', 16, kwargs))
    label.grid(sticky=W, column=0, row=row)


def dump_cookies(driver, fp):
    cookies = driver.get_cookies()
    # TODO: создать переменную с куки-файлом
    # TODO: проверку авторизации сделать
    with open(fp, 'w') as cookie_file:
        json.dump(cookies, cookie_file)


def check_cookie_exist(fp):
    if os.path.isfile(fp) and os.path.getsize(fp):
        return True
    else:
        return False


def dump_in_my_file(info, fp):
    with open(fp, 'w', encoding='utf8') as file:
        yaml.dump(info, file, allow_unicode=True)


def raise_error_about_authorization():
    message = 'Сейчас вам необходимо авторизироваться. Эту процедуру нужно пройти один раз. В будущем авторизация будет проходить автоматически. Как только залогинитесь, нажмите "ok"'
    messagebox.showinfo(title='Введите данные на странице HH', message=message)
    root.update()


# def check_if_info_been_changed(search_key, region, search_period, items_on_page, order):
#     if search_key != search_key_from_file or region != region_from_file or search_period != search_period_from_file or items_on_page != items_on_page_from_file or order != order_from_file:
#         return True
#     else:
#         return False


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
    messagebox.showinfo(title='Название', message=info_str)
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

    driver = webdriver.Chrome('/home/valera/PycharmProjects/HH_auto_mailling/chromedriver')

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
        # TODO: удалить логгирование
        logger.debug(type(SearchPage.next_page_button))
        logger.debug(SearchPage.next_page_button)
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
root.wm_attributes('-alpha', 0.7)
root.geometry('300x851')
root.resizable(width=True, height=True)

# холст для вывода графич. примитивов. Не явл. обязательным
# canvas = Canvas(root, height=300, width=250).pack()

# рамка, содержащая другие графич. компоненты
frame = Frame(root, bg='#F3F5F4')
# relwidth=1, relheight=1 на всю ширину и высоту, relx и rely - смещение. Все это в процентах
frame.place(relwidth=1, relheight=1, relx=0.10, rely=0.05)

label = Label(frame, text='Введите свои данные', bg='#F3F5F4', justify=LEFT)

label.config(font=('PT Sans Caption', 16, 'bold'))

label.grid(sticky=W, column=0, row=0, pady=28)

create_label('Ключевые слова', 1)

searchKeyInput = create_input(search_key_from_file)
searchKeyInput.grid(sticky=W, column=0, row=2)

create_label('Название вашего резюме', 3)

resumeNameInput = create_input(resume_name_from_file)
resumeNameInput.grid(sticky=W, column=0, row=4)

create_label('Регион', 5)

regionInput = create_input(region_from_file)
regionInput.grid(sticky=W, column=0, row=6)

create_label('Введите сопроводительное письмо', 7)

coveringLetterInput = create_input(covering_letter_from_file)
coveringLetterInput.grid(sticky=W, column=0, row=8)

create_label('Сортировка', 9)

ORDER = [
    ('По дате изменения', 'publication_time', 10),
    ('По убыванию зарплат', 'salary_desc', 11),
    ('По возрастанию зарплаты', 'salary_inc', 12),
    ('По соответствию', 'relevance', 13),
]

r_order = StringVar()
r_order.set(order_from_file)

create_radio(ORDER, r_order)

create_label('Выводить', 14)

SEARCH_PERIOD = [
    ('За всё  время', 0, 15),
    ('За месяц', 30, 16),
    ('За неделю', 7, 17),
    ('За последние три дня', 3, 18),
    ('За сутки', 1, 19),
]

r_search_period = IntVar()
r_search_period.set(search_period_from_file)

create_radio(SEARCH_PERIOD, r_search_period)

create_label('Показать на странице', 20)

ITEMS_ON_PAGE = [
    ('20 вакансий', 20, 21),
    ('50 вакансий', 50, 22),
    ('100 вакансий', 100, 23),
]

r_items_on_page = IntVar()
r_items_on_page.set(items_on_page_from_file)

create_radio(ITEMS_ON_PAGE, r_items_on_page)

btn = Button(frame, text='Начать рассылку', bg='#F7C87E', command=btn_click, justify=LEFT,
             border=0)
btn.config(height=2, width=15)
# btn.pack()
btn.grid(sticky=W, column=0, row=24, pady=28)

root.mainloop()
