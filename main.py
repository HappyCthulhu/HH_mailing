import json
import re
import sys
import os
from datetime import datetime

import yaml
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from logging_dir.logging import my_exception_hook, set_logger

from locators import AdvancedSearchLocators, VacancyPage, SearchPage, CommonLocators


def check_driver_exist(fp):
    if os.path.isfile(fp):
        return True
    else:
        return False


def first_json_dump(fp):
    first_json_dump_dict = {
        "count_of_responses": 0,
        "last_block_time": "2000-01-01, 00:00:00",
        "last_mail_time": "2000-01-01  00:00:00.000000"
    }
    with open(fp, 'w', encoding='utf8') as file:
        json.dump(first_json_dump_dict, file, ensure_ascii=False, indent=4)


def check_authorization(driver):
    if check_element_exist(driver, CommonLocators.account_icon):
        return True
    else:
        return False


def set_driver_and_ac(fp):
    driver = webdriver.Chrome(fp)
    AC = ActionChains(driver)
    return driver, AC


def unpack_info_file(fp):
    with open(fp, 'r') as file:
        file_dict = yaml.load(file, Loader=yaml.FullLoader)
        return file_dict


def click(driver, xpath):
    driver.find_element_by_xpath(xpath).click()


def send_keys(driver, xpath, keys):
    driver.find_element_by_xpath(xpath).send_keys(keys)


def find_element_by_xpath(driver, xpath):
    return driver.find_element_by_xpath(xpath)


def move_to_elem_by_xpath(driver, xpath):
    return driver.execute_script('arguments[0].scrollIntoView(true);',
                                 driver.find_element_by_xpath(xpath))


def unpack_about_mailing_file(fp):
    with open(fp, 'r') as file:
        file_dict = json.load(file)

    return file_dict


def dump_about_mailing_in_file(fp, dict):
    with open(fp, 'w', encoding='utf8') as file:
        json.dump(dict, file, ensure_ascii=False, indent=4)


def unpack_dict(dict):
    search_key = dict.get('search_key')
    region = dict.get('region')
    search_period = dict.get('search_period')
    resume_name = dict.get('resume_name')
    items_on_page = dict.get('items_on_page')
    order = dict.get('order')
    covering_letter = dict.get('covering_letter')

    return search_key, resume_name, region, search_period, items_on_page, order, covering_letter


def send_cookies(driver, fp):
    with open(fp, 'r') as cookie_file:
        cookies_from_file = json.load(cookie_file)

    for cookie in cookies_from_file:
        driver.add_cookie(cookie)
    return driver


def fill_advanced_search_settings_page(driver, search_key, region, search_period, items_on_page,
                                       order_from_file):
    if check_if_there_one_day_passed_after_block(LAST_BLOCK_TIME):
        logger.critical('Не прошло одного дня с последней блокировки рассылки!\n'
                        'Вы уверены, что хотите продолжить?\n'
                        'Ниже введите без кавычек "y", если да и "n", если нет')
        respond = input()
        if respond == 'n':
            sys.exit()

    driver.get('https://spb.hh.ru/account/login?backurl=%2F')

    # if not find_element_by_xpath('//span[@data-qa="expand-login-by-password"]'):
    #
    #     send_keys(LoginPage.login_without_pass, login)
    #     send_keys(LoginPage.password, password)
    #     time.sleep(10)
    # click(LoginPage.enter_button)
    #     click(LoginPage.enter_button)

    # else:

    # set Advanced Search

    driver.get('https://spb.hh.ru/search/vacancy/advanced')

    send_keys(driver, AdvancedSearchLocators.keywords, search_key)

    # находим все выбранные места (города/регионы/страны)
    if driver.find_elements_by_xpath(
            AdvancedSearchLocators.list_of_places):

        # TODO: какого хуя не работает move_by_offset, а move_to_element работает ебано
        for _ in range(len(driver.find_elements_by_xpath(AdvancedSearchLocators.list_of_places))):
            move_to_elem_by_xpath(driver, AdvancedSearchLocators.list_of_places)

            click(driver, AdvancedSearchLocators.list_of_places)

    send_keys(driver, AdvancedSearchLocators.region, region)

    # если не промотать вниз, элемент не будет активен
    # TODO: А время точно так работает, а не обнуляется ровно в 00?

    a.search_period = search_period
    search_period = a.search_period

    a.items_on_page = items_on_page
    items_on_page = a.items_on_page

    a.order = order_from_file
    sort_by = a.order

    move_to_elem_by_xpath(driver, sort_by)

    click(driver, sort_by)
    click(driver, search_period)
    click(driver, items_on_page)

    # TODO: изменить везде классы на экземпляры классов
    click(driver, a.search_button)

    logger.debug('Настроили поиск. Начинаем рассылку вакансий')

    # TODO: подрубить логгирование: "Для отклика нужно пройти текст" или "для вакансии нужен более расширенный отклик"
    # TODO: понять, почему вакансий больше 100


def logging_final_results(number_of_responses, number_of_pages, message=None):
    if message:
        logger.info(message)
    logger.info('Работа успешно выполнена\n'
                f'Количество откликов: {number_of_responses}\n'
                f'Количество обработанных страниц: {number_of_pages}')


def check_element_exist(driver, xpath, wait_time=None):
    # TODO: проверить, норм ли это работает
    # TODO: нихуя это нормально не работает
    if wait_time:
        try:
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
    else:
        try:
            find_element_by_xpath(driver, xpath)
            return True
        except NoSuchElementException:
            return False


def get_vacancy_id_and_link(element):
    vacancy_id_list = re.findall('(?<=vacancy/).+?(?=")', element)
    if vacancy_id_list:
        vacancy_id = vacancy_id_list[0]
        vacancy_link = f'https://spb.hh.ru/applicant/vacancy_response?vacancyId={vacancy_id}'

        return vacancy_id, vacancy_link
    else:
        logger.critical('Регулярки не нашли id.\n'
                        f'{element}')
        return None, None


# def choose_resume(my_resume_name, list_of_resumes):
#     for resume_from_list in list_of_resumes:
#         if resume_from_list.text != my_resume_name:
#             continue
#         else:
#             return resume_from_list
#     logger.critical('Не нашел нужного резюме. Проверьте, правильно ли написали название вашего резюме\n'
#                     f'Введенное вами название: {my_resume_name}')


# TODO: сделать функцию, которая высчитывает разницу во времени с последнего блокировки
def check_if_there_one_day_passed_after_block(previous_time):
    # TODO: найти способ красиво записывать это без tuple
    now = datetime.now()
    previous_time = now.strptime(previous_time, "%Y-%m-%d, %H:%M:%S")
    time_difference = datetime.now() - previous_time
    if time_difference.days < 1:
        return True
    else:
        return False


def dump_vacancies_data_in_file(fp, *block_time):
    file_dict = unpack_about_mailing_file(fp)

    if block_time:
        file_dict['last_block_time'] = block_time[0]
    else:
        file_dict['count_of_responses'] += 1
        file_dict['last_mail_time'] = str(datetime.now())

    dump_about_mailing_in_file(ABOUT_MAILING_FILE, file_dict)


# TODO: Настроить рассылку по заданному количеству откликов
# TODO: разбить на большее количество функций
def dump_vacancies_with_extra_questions_in_file(link, fp):
    if os.path.isfile(VACANCIES_WITH_EXTRA_QUESTIONS):
        with open(fp, 'r', encoding='utf-8') as file:
            file_info = yaml.load(file, Loader=yaml.FullLoader)
        file_info.append(link)
    else:
        file_info = [link]
    with open(fp, 'w', encoding='utf8') as file:
        yaml.dump(file_info, file, encoding=None, allow_unicode=True)


def process_vacancy_page(driver, link, vacancy_number, resume_name, fp_info_file, covering_letter_from_file,
                         number_of_responses, number_of_pages):
    window_before = driver.window_handles[0]

    driver.execute_script('''window.open();''')

    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    driver.get(link)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, VacancyPage.send_request_header)))

    if check_element_exist(driver, VacancyPage.vacancy_with_questionnaire):
        logger.info('Вакансия требуется дополнительной хуйни')
        # проверить работу
        dump_vacancies_with_extra_questions_in_file(link, VACANCIES_WITH_EXTRA_QUESTIONS)
    elif check_element_exist(driver, VacancyPage.vacancy_with_extra_questions):
        logger.info('Вакансия требует ответов на дополнительные вопросы')
        dump_vacancies_with_extra_questions_in_file(link, VACANCIES_WITH_EXTRA_QUESTIONS)

    else:

        v.resume_name = resume_name
        resume_name_xpath = v.resume_name
        if not check_element_exist(driver, resume_name_xpath):
            logger.critical('Не нашел нужного резюме. Проверьте, правильно ли написали название вашего резюме\n'
                            f'Введенное вами название: {resume_name}')
        click(driver, resume_name_xpath)

        if check_element_exist(driver, VacancyPage.covering_letter_button):
            click(driver, VacancyPage.covering_letter_button)

        send_keys(driver, VacancyPage.covering_letter_input, covering_letter_from_file)
        click(driver, VacancyPage.respond_button)
        dump_vacancies_data_in_file(ABOUT_MAILING_FILE)
        # TODO: мб сделать проверку на блокировку по кратности количества откликов?
        # TODO: сделать проверку на блокировку отдельной функцией
        if vacancy_number % 10 == 0 and check_element_exist(
                driver, VacancyPage.negotiations_limit_exceed_div, 5):
            # TODO: регулярки рекламу не находят, а мб должны
            logging_final_results(number_of_responses, number_of_pages, message='Исчерпан лимит откликов за день')
            now = datetime.now()
            time_now = now.strftime("%Y-%m-%d, %H:%M:%S")
            dump_vacancies_data_in_file(fp_info_file, time_now)
            sys.exit()

        # except TimeoutException:
        #     pass

    driver.close()

    driver.switch_to.window(window_before)


def send_responses_on_page(driver, resume_name, fp_info_file, covering_letter_from_file, number_of_responses,
                           number_of_pages):
    list_of_vacancies = driver.find_elements_by_xpath(SearchPage.list_of_vacancies)

    vacancy_number = 0

    for element in list_of_vacancies:

        element_html = element.get_attribute('innerHTML')
        vacancy_number += 1

        if 'class="search-resume-item-label search-resume-item-label_responded"' in element_html or 'class="search-resume-item-label search-resume-item-label_invited"' in element_html or 'class="search-resume-item-label search-resume-item-label_discard"' in element_html:
            continue

        vacancy_id, vacancy_link = get_vacancy_id_and_link(element_html)
        if not vacancy_id:
            continue
        logger.debug(f'{vacancy_number}/{len(list_of_vacancies)}: {vacancy_link}')

        process_vacancy_page(driver, vacancy_link, vacancy_number, resume_name, fp_info_file, covering_letter_from_file,
                             number_of_responses, number_of_pages)


ABOUT_MAILING_FILE = 'about_mailing.json'

VACANCIES_WITH_EXTRA_QUESTIONS = 'vacancies_with_extra_questions.yml'

if not os.path.isfile(ABOUT_MAILING_FILE):
    first_json_dump(ABOUT_MAILING_FILE)

ABOUT_MAILING_FILE_DICT = unpack_about_mailing_file(ABOUT_MAILING_FILE)
LAST_BLOCK_TIME = ABOUT_MAILING_FILE_DICT['last_block_time']
sys.excepthook = my_exception_hook
set_logger()

a = AdvancedSearchLocators()
v = VacancyPage()
