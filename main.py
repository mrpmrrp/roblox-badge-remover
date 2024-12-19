import json, requests, os

from platform import system
from colorama import Fore, init
from typing import List

init()

with open('config.json', 'r') as file:
    config= file.read()
    config= json.loads(config)

    file.close()
    del file

def fetch_badges(UserId: int) -> List[str]:
    Badges = []
    next_page_cursor = ''

    while True:
        response: requests.Response = requests.get(f'https://badges.roblox.com/v1/users/{UserId}/badges?limit=10&cursor={next_page_cursor}&sortOrder=Asc')
        response_json: json = response.json()

        [Badges.append(cell.get('id')) for cell in response_json.get('data')]
        next_page_cursor = response_json.get('nextPageCursor')
        if next_page_cursor is None:
            break
    
    return Badges

def fetch_csrf(Cookie: str) -> str:
    return requests.post('https://auth.roblox.com/v2/logout', cookies= {'.ROBLOSECURITY': Cookie}).headers.get('x-csrf-token')

def delete_badge(Cookie: str, BadgeId: int) -> None:
    csrf: requests.Response = fetch_csrf(Cookie)

    try:
        response: requests.Response = requests.delete(f'https://badges.roblox.com/v1/user/badges/{BadgeId}', headers= { 'X-CSRF-TOKEN': csrf }, cookies={".ROBLOSECURITY": Cookie})
        if (response.status_code != 200):
            raise Exception(response.json().get('errors')[0]['message'])
        print(Fore.GREEN + f'Deleted {BadgeId}')
    except Exception as error_message: 
        print(f'{error_message}')
    finally:
        response.close()


def main(Cookie: str) -> None:
    user_data = requests.get('https://users.roblox.com/v1/users/authenticated', cookies={ ".ROBLOSECURITY": Cookie })
    UserId: int = user_data.json().get('id')   
    Username: str = user_data.json().get('name')

    print(f'Logged in as {Username}')
    
    Badges: List[str]= fetch_badges(UserId)
    [delete_badge(Cookie=Cookie, BadgeId=Badge) for Badge in Badges]


if __name__ == '__main__':
    os.system('cls' if (system().lower() == 'windows') else 'clear')
    
    Cookie= config.get('Cookie')
    if len(Cookie) < 1:
        print('Invalid cookie')
        exit()

    main(Cookie)
