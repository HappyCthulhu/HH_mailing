class CommonLocators:
    account_icon = '//span[@class="supernova-icon supernova-icon_profile HH-Supernova-Menu-ArrowAnchor"]'

class LoginPage:
    login = '//div/input[@name="username"]'
    login_without_pass = '//div/input[@name="login"]'
    password = '//span/input[@type="password"]'
    enter_button = '//button[@class="bloko-button bloko-button_primary bloko-button_stretched"]'

class AdvancedSearchLocators:
    def __setattr__(self, setting_search, value):
        if setting_search == 'items_on_page':
            value = f'//label[@data-qa="control-search__items-on-page control-search__items-on-page_{value}"]'

        elif setting_search == 'search_period':
            # available: 0 (all time), 1, 3, 7, 30
            value = f'//label[@data-qa="control-vacancysearch__searchperiod-item control-vacancysearch__searchperiod-item_{value}"]'

        elif setting_search == 'order':
            # available salary_desc, relevance, salary_asc, publication_time
            value = f'//label[@data-qa="control-search__order control-search__order_{value}"]'

        self.__dict__[setting_search] = value

    keywords = '//input[@id="advancedsearchmainfield"]'
    region = '//input[@class="bloko-input                                         Bloko-CompositeSelection-Suggest                                         jsxComponents-Hint-Input"]'
    search_button = '//input[@id="submit-bottom"]'
    list_of_places = '//span[@class="Bloko-CompositeSelection-TagList"]/span[contains(@data-qa, "bloko-tag")]/span[@class="bloko-icon-dynamic"]'

class SearchPage:
    next_page_button = '//a[@data-qa="pager-next"]'
    list_of_vacancies = '//div[contains(@class, "vacancy-serp-item") and contains(@data-qa, "vacancy-serp__vacancy")]'

class VacancyPage:
    def __setattr__(self, items, value):
        if items == 'resume_name':
            value = f"//*[contains(text(), '{value}')]"

        self.__dict__[items] = value

    list_of_resumes = '//span[@class="bloko-radio__text"]'
    covering_letter_button = '//span[@class="bloko-link-switch"]'
    covering_letter_input = '//textarea[@data-qa="vacancy-response-popup-form-letter-input"]'
    respond_button = '//button[@class="bloko-button bloko-button_primary"]'
    vacancy_with_questionnaire = '//h2[@class="vacancy-response-popup-title"]'
    vacancy_with_extra_questions = '//p[@data-qa="employer-asking-for-test"]'
    send_request_header = '//h1[@data-qa="bloko-header-1"]'
    negotiations_limit_exceed_div = '//div[@data-qa-popup-error-code="negotiations-limit-exceeded"]'