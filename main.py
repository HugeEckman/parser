import requests as rq
from bs4 import BeautifulSoup as bs

endpoint = 'https://otus.ru/nest/post/108/'

def get_domain(endpoint: str) -> str:
    split_endpoint = endpoint.split('/')
    return f'{split_endpoint[0]}//{split_endpoint[2]}'

def get_refs(endpoint: str) -> list:
    response = rq.get(endpoint)
    refs = []
    soup = bs(response.text, 'html.parser')

    a_tags = soup.find_all('a')
    
    for item in a_tags:
        if not item.has_attr('href'):
            continue
        refs.append(item['href'])

    return refs

def print_refs(endpoint: str, is_print_to_file: bool) -> None:

    first_level_refs = get_refs(endpoint=endpoint)

    domain = get_domain(endpoint)

    intend = '    '

    list_of_refs = []

    for ref in first_level_refs:
        if is_print_to_file:
            list_of_refs.append(ref)
        else:
            print(ref)
        if not ref.startswith('/') and not ref.startswith('http'):
            continue
        elif ref.startswith('/'):
            endpoint = domain + ref
            second_level_refs = get_refs(endpoint=endpoint)
            for item in second_level_refs:
                if is_print_to_file:
                    list_of_refs.append(ref)
                else:
                    print(f'{intend}{item}')
        elif ref.startswith('http'):
            endpoint = ref
            second_level_refs = get_refs(endpoint=endpoint)
            for item in second_level_refs:
                if is_print_to_file:
                    list_of_refs.append(ref)
                else:
                    print(f'{intend}{item}')

    if is_print_to_file:
        with open('all_refs', 'w') as file:
            file.writelines(list_of_refs)

print_refs(endpoint=endpoint, is_print_to_file=True)



