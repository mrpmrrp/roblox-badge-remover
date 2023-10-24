import requests, asyncio

Cookie = input('Enter your ROBLOX account cookie:   ')

if (Cookie.startswith('.ROBLOSECURITY=') != True):
    Cookie = f'.ROBLOSECURITY={Cookie}'

global user_data
with requests.get('https://www.roblox.com/mobileapi/userinfo', headers = { 'Cookie': Cookie}) as validation_response:
    try:
        user_data = validation_response.json()
        
        global user_id

        # user_id  = response_json['UserId']
        username = user_data['UserName']
        user_id = user_data['UserID']

        print(f'Logged in as: {username} ({user_id})') 
    except:
        print('fatal error')
        exit()

async def get_token():
    response = requests.post('https://auth.roblox.com/v2/logout', headers = { 'Cookie': Cookie })
    return response.headers.get('x-csrf-token')

async def get_badges(user_id, token):
    response = requests.get(f'https://badges.roblox.com/v1/users/{user_id}/badges', headers = {
        'Cookie': Cookie,
        'x-csrf-token': token,
        'content-type': 'application/json'
    })

    return response.json()

async def remove_badge(badge_id, token):
    response = requests.delete(f'https://badges.roblox.com/v1/user/badges/{badge_id}', headers = {
        'Cookie': Cookie,
        'x-csrf-token': token
    })

    print(f'badge id: {badge_id} - response code {response}')

async def main():
    print('Starting.. please wait.')

    while True:
        Token = await get_token()

        AllBadges = await get_badges(user_data['UserID'], Token)
        Badges = AllBadges['data']
        
        if len(Badges) < 1:
            break

        for Badge in Badges:
            await remove_badge(Badge['id'], Token)
    
    print('Done! exiting.')
    exit()

if __name__ == '__main__':
    asyncio.run(main())