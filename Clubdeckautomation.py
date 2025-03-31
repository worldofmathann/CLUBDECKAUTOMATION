import requests
import os
import json
import time
import datetime
import re
from colorama import Fore, Style, init
init()

header = [
    r"  _________   ___ ___              _____   ____ ______________________      _____      ________________.___________    _______   ",
    r"/_   ___ \ /   |   \            /  _  \ |    |   \__    ___/\_____  \    /     \    /  _  \__    ___/|   \_____  \   \      \  ",
    r"/    \  \//    ~    \  ______  /  /_\  \|    |   / |    |    /   |   \  /  \ /  \  /  /_\  \|    |   |   |/   |   \  /   |   \ ",
    r"\     \___\    Y    / /_____/ /    |    \    |  /  |    |   /    |    \/    Y    \/    |    \    |   |   /    |    \/    |    \ ",
    r" \______  /\___|_  /          \____|__  /______/   |____|   \_______  /\____|__  /\____|__  /____|   |___\_______  /\____|__  /",
    r"        \/       \/                   \/                            \/         \/         \/                     \/         \/ ",

    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>",
    r"                               CLUBDECK AUTOMATION CODE WITH AUTOUPDATED FEATURE V2.0",
    r"    CH Username: @_worldofmathan                                                      Telegram Username: @worldofmathan",
    r"                                  Telegram Group Link : https://t.me/clubhouseapps",
    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"

]

print(f"{Fore.RED}{header[0]}")
print(f"{Fore.GREEN}{header[1]}")
print(f"{Fore.YELLOW}{header[2]}")
print(f"{Fore.BLUE}{header[3]}")
print(f"{Fore.MAGENTA}{header[4]}")
print(f"{Fore.CYAN}{header[5]}")
print(f"{Fore.LIGHTBLUE_EX}{header[6]}")
print(f"{Fore.LIGHTCYAN_EX}{header[7]}")
print(f"{Fore.LIGHTCYAN_EX}{header[8]}")
print(f"{Fore.LIGHTCYAN_EX}{header[9]}")
print(f"{Fore.LIGHTBLUE_EX}{header[10]}")
print(Style.RESET_ALL)


APPDATA_PATH = os.getenv('APPDATA', '')
CLUBDECK_FILENAME = os.path.join(APPDATA_PATH, 'Clubdeck', 'profile.json')
SANDBOX_PATH = "C:/Sandbox/"

def get_profile_token(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                return data.get('token'), data['user'].get('name')
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading profile: {e}")
    return None, None

def extract_tokens_from_clubdeck(filename):
    return get_profile_token(filename)

def extract_tokens_from_sandbox():
    extracted_data = []

    for root, dirs, files in os.walk(SANDBOX_PATH):
        for file in files:
            if file == "profile.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        profile_data = json.load(f)
                        if 'token' in profile_data and 'user' in profile_data:
                            token = profile_data.get("token")
                            user_name = profile_data.get("user").get("name")
                            extracted_data.append({"token": token, "user_name": user_name})
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error decoding sandbox profile.json: {e}")

    if extracted_data:
        print("Select a name by entering the corresponding index:")
        for idx, data in enumerate(extracted_data):
            print(f"{idx + 1}. {data['user_name']}")

        try:
            selected_idx = int(input("Enter the index of the name you want to select: ")) - 1
            selected_data = extracted_data[selected_idx]
            return selected_data['token'], selected_data['user_name']
        except (ValueError, IndexError):
            print("Invalid selection.")
    else:
        print("No valid profile.json files found in Sandbox.")
    return None, None

def manual_token_entry():
    auth_token = input("Enter the manual token: ")
    try:
        response = requests.post('https://www.clubhouseapi.com/api/me',
                                 headers={'Authorization': f'Token {auth_token}'})
        response.raise_for_status()
        name = response.json()['user_profile']['name']
        print("Manual token entry successful.")
        return auth_token, name
    except requests.RequestException as e:
        print(f"Error during manual token entry: {e}")
    return None, None

def extract_tokens_and_names():
    print("Select an option:")
    print("1. Sync With Clubdeck")
    print("2. Use SandBoxie Accounts")
    print("3. Manually Enter Token")

    option = input("Enter your choice (1/2/3): ")
    if option == '1':
        return extract_tokens_from_clubdeck(CLUBDECK_FILENAME)
    elif option == '2':
        return extract_tokens_from_sandbox()
    elif option == '3':
        return manual_token_entry()
    else:
        print("Invalid option. Please select 1, 2, or 3.")
        return None, None

def search_user(username, token):
    url = "https://www.clubhouseapi.com/api/search_users"
    headers = {'Authorization': f"Token {token}"}
    data = {"query": username}
    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        json_data = resp.json()
        users = json_data.get('users', [])
        for user in users:
            if user.get('username') == username:
                user_id = user.get('user_id')
                name = user.get('name')
                return user_id, name
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    except ValueError as ve:
        print(f"Error decoding JSON: {ve}")
        return None, None

def get_profile(user_id, token):
    url = "https://www.clubhouseapi.com/api/get_profile"
    headers = {"Authorization": f"Token {token}"}
    payload = {"user_id": user_id}
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        if 'user_profile' in data:
            user_profile = data['user_profile']
            user_id = user_profile.get('user_id')
            name = user_profile.get('name')
            displayname = user_profile.get('displayname')
            username = user_profile.get('username')
            num_followers = user_profile.get('num_followers')
            num_following = user_profile.get('num_following')
            time_created = user_profile.get('time_created')
            if time_created:
                time_created = datetime.datetime.strptime(time_created, "%Y-%m-%dT%H:%M:%S.%f%z")
                formatted_time_created = time_created.strftime("%d-%B-%Y %H:%M")
            else:
                formatted_time_created = "N/A"
            photo_url = user_profile.get('photo_url')
            return user_id, name, displayname, username, num_followers, num_following, formatted_time_created, photo_url
        else:
            print("User profile not found in response.")
            return None, None, None, None, None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None, None, None, None, None, None, None
    except ValueError as ve:
        print(f"Error decoding JSON: {ve}")
        return None, None, None, None, None, None, None, None

def download_profile_picture(photo_url, save_path):
    try:
        response = requests.get(photo_url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("Profile picture downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading profile picture: {e}")

def update_username(username, token):
    url = "https://www.clubhouseapi.com/api/update_name"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "name": username
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Name updated successfully!")
    else:
        print("Failed to update username. Error:", response.text)

def update_display_name(new_name, token):
    url = "https://www.clubhouseapi.com/api/update_displayname"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "name": new_name
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Display name updated successfully!")
    else:
        print("Failed to update display name. Error:", response.text)

def update_userid(user_id, token):
    url = "https://www.clubhouseapi.com/api/update_username"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "username": user_id
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("User ID updated successfully!")
    else:
        print("Failed to update User ID. Error:", response.text)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def send_phone_number(phone_number, api_token):
    url = "https://www.clubhouseapi.com/api/perform_hyperview_action"
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "action_name": "settings/account/phone_number.xml",
        "pixel_ratio": 2.55,
        "visual_style": "light",
        "params": json.dumps({"phone_number": phone_number})
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f" OTP Sent Successfully For {phone_number} ....!")
            response_json = response.json()
            if 'view' in response_json:
                view_content = response_json['view']
                match = re.search(r'session_id=(.*?)"', view_content)
                if match:
                    session_id = match.group(1)
                    return session_id
                else:
                    print("Session ID not found in the response.")
                    return None
            else:
                print("No 'view' key found in the response.")
                return None
        else:
            print(f"Failed to send OTP. Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def verify_code(session_id, verification_code, api_token, phone_number):
    url = "https://www.clubhouseapi.com/api/perform_hyperview_action"
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "action_name": "settings/account/phone_code/verify_code.xml",
        "pixel_ratio": 2.55,
        "visual_style": "light",
        "params": json.dumps({"session_id": session_id, "code": verification_code})
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Phone Number Successfully Changed To {phone_number} ....!")
        else:
            print(f"Failed to verify code. Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    print("\nSelect an option:")
    print("1. Update Name")
    print("2. Update Alias Name")
    print("3. Update User Name")
    print("4. Change Phone Number")
    print("5. Download Profile Info")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == "4":
        token, botname = extract_tokens_and_names()
        if not token:
            print("Token extraction failed. Exiting.")
            time.sleep(3)
            return

        print(f"\nWelcome << {botname} >> is Syncing...")

        phone_number = input("Please enter the phone number: ")
        session_id = send_phone_number(phone_number, token)
        if session_id:
            verification_code = input("Please enter the verification code: ")
            verify_code(session_id, verification_code, token, phone_number)
        return

    token, botname = extract_tokens_and_names()
    if not token:
        print("Token extraction failed. Exiting.")
        time.sleep(3)
        return

    print(f"\nWelcome << {botname} >> is Syncing...")

    if choice == "1":
        username = input("Enter your desired username: ")
        update_username(username, token)

    elif choice == "2":
        new_name = input("Enter the new display name: ")
        update_display_name(new_name, token)

    elif choice == "3":
        user_id = input("Enter the new user Name: ")
        update_userid(user_id, token)

    elif choice == "5":
        username_to_search = input("Enter the username (without @) to search: ")
        user_id, name = search_user(username_to_search, token)
        if user_id:
            profile_info = get_profile(user_id, token)
            if profile_info:
                user_id, name, displayname, username, num_followers, num_following, formatted_time_created, photo_url = profile_info
                safe_name = sanitize_filename(name)
                with open(f"profilewith_{safe_name}.txt", 'w', encoding='utf-8') as f:
                    f.write(f"User ID: {user_id}\n")
                    f.write(f"Name: {name}\n")
                    f.write(f"Display Name: {displayname}\n")
                    f.write(f"Username: {username}\n")
                    f.write(f"Number of Followers: {num_followers}\n")
                    f.write(f"Number of Following: {num_following}\n")
                    f.write(f"Profile Created: {formatted_time_created}\n")

                if photo_url:
                    picture_path = f"{safe_name}_profile_picture.jpg"
                    download_profile_picture(photo_url, picture_path)
            else:
                print("Failed to retrieve profile information.")
        else:
            print("User not found.")

if __name__ == "__main__":

    main()
