from ..db.cls import Database
"""
in this file  we handle  users:


"""

db = Database()


async def user_login(user_info):

    # todo: add a field to indicate source system for auth, like aichat, dashboard,...
    # todo: rename user_id_platform to source_user_id

    # if user doesnt registered, register it and return user_id
    # else return user_id

    # user_id_platform = user_info["id"]
    # first_name = user_info["first_name"]
    # last_name = user_info["last_name"]
    # username = user_info[""]

    source_system_id = 1  # 1 indicate social_chat_bot system
    user_id = await get_user_id(source_user_id=user_info["id"],
                                source_system_id=source_system_id)
    if user_id:
        print("get_user_id", user_id)
    else:
        user_id = await create_new_user(source_user_id=user_info["id"], first_name=user_info["first_name"], last_name=user_info["last_name"],
                                        username=user_info["username"], source_system_id=source_system_id)
        print("create_new_user", user_id)
    return user_id


# ----------------------------------------------------
async def get_user_id(source_user_id, source_system_id):

    query = """
    SELECT text FROM auth.users where source_user_id = {source_user_id} and \
        source_system_id = {source_system_id}
        """
    result = await db.execute_select(query, {})
    return result

# ----------------------------------------------------


async def create_new_user(source_user_id, first_name, last_name,
                          username, source_system_id):

    await db.connect()
    new_user_id = await db.execute_insert(
        query=f"INSERT INTO auth.users (source_user_id, first_name, last_name, username, source_system_id) \
            VALUES ({source_user_id}, '{first_name}', '{last_name}', '{username}', {source_system_id})",
        params={}
    )

    # new_user_id = await db.execute_insert(
    #     query="""INSERT INTO auth.users 
    #             (source_user_id, first_name, last_name, username, source_system_id) 
    #             VALUES ($1, $2, $3, $4, $5)""",
    #     params={
    #         'source_user_id': 123,
    #         'first_name': 'John',
    #         'last_name': 'Doe',
    #         'username': 'johndoe',
    #         'source_system_id': 1
    #     }
    # )

    return new_user_id

# ----------------------------------------------------


async def disable_user():
    pass
