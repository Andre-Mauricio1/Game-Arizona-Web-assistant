import sqlite3


async def Bd_add_users():
    with sqlite3.connect() as db:
        with db.cursor() as cursor:
            pass

    return db, cursor

# В БУДУЩЕМ ДОБАВЛЮ, ПУСТЬ ЛЕЖИТ НЕ РЫПАЕТСЯ