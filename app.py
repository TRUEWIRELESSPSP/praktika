import redis

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Очистка БД на случай повторного запуска
r.flushdb()

# Данные клубов
clubs = {
    1: {"name": "Звезда", "city": "Москва", "founded": 1995},
    2: {"name": "Вихрь", "city": "Казань", "founded": 2003},
    3: {"name": "Олимп", "city": "Сочи", "founded": 2010},
    4: {"name": "Барс", "city": "Новосибирск", "founded": 1998}
}

# Данные видов спорта
sports = {
    1: "Футбол",
    2: "Баскетбол",
    3: "Волейбол",
    4: "Хоккей",
    5: "Гандбол"
}

# Связи между клубами и видами спорта
club_sports = {
    1: [1, 2],         # Звезда: футбол, баскетбол
    2: [2, 3, 5],      # Вихрь: баскетбол, волейбол, гандбол
    3: [1, 3, 4],      # Олимп: футбол, волейбол, хоккей
    4: [2, 4]          # Барс: баскетбол, хоккей
}

# Добавляем клубы
for club_id, data in clubs.items():
    key = f"club:{club_id}"
    r.hset(key, mapping=data)

# Добавляем виды спорта
for sport_id, name in sports.items():
    key = f"sport:{sport_id}"
    r.hset(key, mapping={"name": name})

# Создаём связи между клубами и видами спорта
for club_id, sport_ids in club_sports.items():
    for sport_id in sport_ids:
        r.sadd(f"club:{club_id}:sports", sport_id)
        r.sadd(f"sport:{sport_id}:clubs", club_id)

# Вывод: клубы и их виды спорта
print("\n📌 Виды спорта по клубам:")
for club_id in clubs:
    club = r.hgetall(f"club:{club_id}")
    sport_ids = r.smembers(f"club:{club_id}:sports")
    sport_names = [r.hget(f"sport:{sid}", "name") for sid in sport_ids]
    print(f"- {club['name']} ({club['city']}): {', '.join(sport_names)}")

# Вывод: клубы по каждому виду спорта
print("\n📌 Клубы по видам спорта:")
for sport_id in sports:
    sport_name = r.hget(f"sport:{sport_id}", "name")
    club_ids = r.smembers(f"sport:{sport_id}:clubs")
    club_names = [r.hget(f"club:{cid}", "name") for cid in club_ids]
    print(f"- {sport_name}: {', '.join(club_names)}")
