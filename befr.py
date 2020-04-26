import vk_api


def auth_handler():
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    login, password = ''
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    candidates = {}

    for suggestion in vk.friends.getSuggestions(count=500)['items']:
        if suggestion['id'] not in candidates:
            candidates[suggestion['id']] = suggestion

    for _ in range(1):
        for candidate in list(candidates.values()):
            try:
                for new_c in vk.friends.get(user_id=candidate['id'])['items']:
                    if new_c not in candidates:
                        candidates[new_c] = {}
            except:
                continue

    for cand_id in candidates.keys():
        info = vk.users.get(user_ids=[str(cand_id)], fields='books,bdate,career,counters')
        print(info)

    # ...


if __name__ == '__main__':
    main()
