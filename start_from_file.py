import json
import os
import time
import sys

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from main import send_cookies, fill_advanced_search_settings_page, check_element_exist, send_responses_on_page, logging_final_results, click, unpack_info_file
from logging_dir.logging import set_logger, my_exception_hook
from locators import SearchPage
set_logger()
sys.excepthook = my_exception_hook

INFO_FILE = 'my_info.yml'
COOKIES_FILE = 'cookies.json'

# TODO: приделать отправку куки

dict_from_file = unpack_info_file(INFO_FILE)
search_key, resume_name, region, search_period_from_file, items_on_page_from_file, order_from_file, last_block_time, count_of_responses, time_from_file = unpack_dict(dict_from_file)

logger.debug(f'Достали из файла: \n'
             f'Ключ поиска вакансии: {search_key}\n'
             f'Название выбранного вами резюме: {resume_name}\n'
             f'Регион: {region}\n'
             f'Количество вакансий на странице: {items_on_page_from_file}\n'
             f'Вакансии отображаются за период в {search_period_from_file} дней (0 - за все время)\n'
             f'Порядок: {order_from_file}')

driver = webdriver.Chrome('/home/valera/PycharmProjects/HH_auto_mailling/chromedriver')
AC = ActionChains(driver)

if not os.path.isfile(COOKIES_FILE) or not os.path.getsize(COOKIES_FILE):
    logger.info(
        'Сейчас вам необходимо авторизироваться. Эту процедуру нужно пройти один раз. В будущем авторизация будет проходить автоматически. Как только залогинитесь, напишите любой символ под этой надписью и нажмите Enter')
    input()
    cookies = driver.get_cookies()
    # TODO: создать переменную с куки-файлом
    # TODO: проверку авторизации сделать
    with open(COOKIES_FILE, 'w') as cookie_file:
        json.dump(cookies, cookie_file)

send_cookies(driver, COOKIES_FILE)
fill_advanced_search_settings_page(driver, search_key, region, search_period_from_file, items_on_page_from_file, order_from_file, last_block_time)

number_of_responses = 0
number_of_pages = 1

# TODO: функция, которая берет общее количество страниц. В пизду пока. Если страниц меньше 6, кнопки с финальной страницей нет.
# TODO: Настроить рассылку по заданному количеству откликов
if check_element_exist(driver, SearchPage.next_page_button):
    while WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, SearchPage.next_page_button))):
        # тут должно располагаться все
        logger.debug(f'Перешли на страницу: {number_of_pages}')

        number_of_pages += 1
        send_responses_on_page(driver)

        click(driver, SearchPage.next_page_button)

else:
    logger.info('Страница всего одна!')
    send_responses_on_page(driver)

time.sleep(4)
logging_final_results(number_of_responses, number_of_pages)
