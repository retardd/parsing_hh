import requests
import fake_headers
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def main():
    headhunter_json = []
    headers_gen = fake_headers.Headers(browser='chrome', os='win')
    r = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0', headers=headers_gen.generate())
    html_data = r.text
    html_parse = BeautifulSoup(html_data, 'html.parser')
    list_items = html_parse.find_all('div', class_='vacancy-serp-item__layout')
    for item in list_items:
        vacancy_json = {}
        session = HTMLSession()
        tag = item.find('a', class_='serp-item__title')
        link_vacancy = tag['href']
        r = session.get(link_vacancy, headers=headers_gen.generate())
        html_data = r.content
        html_parse_vacancy = BeautifulSoup(html_data, 'html.parser')
        body_vacancy = html_parse_vacancy.find('div', class_='g-user-content').text.lower()
        if 'django' in body_vacancy or 'flask' in body_vacancy:
            vacancy_json['vacancy_city'] = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.replace(u'\xa0', u' ')
            vacancy_json['vacancy_company'] = item.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace(u'\xa0', u' ')
            vacancy_json['vacancy_name'] = html_parse_vacancy.find('h1', class_='bloko-header-section-1').text.replace(u'\xa0', u' ')
            vacancy_json['vacancy_link'] = link_vacancy
            salary_info = html_parse_vacancy.find('span', class_='vacancy-salary-compensation-type')
            if salary_info:
                vacancy_json['salary'] = html_parse_vacancy.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text.replace(u'\xa0', u' ')
            else:
                vacancy_json['salary'] = 'Доход не указан'
            headhunter_json.append(vacancy_json)
    print(headhunter_json)


if __name__ == '__main__':
    main()
