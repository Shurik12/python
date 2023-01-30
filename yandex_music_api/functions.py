from tqdm import tqdm

def insert_to_playlist(client, playlist="bards"):
    playlist_map = {
        "Rap": "1015",
        "Classic": "1014",
        "Punk Rock": "1013",
        "Rock and Roll": "1011",
        "Русское народное": "1010",
        "Авторская песня": "1009",
        "КиШ": "1008",
        "Pop": "1007",
        "Tango": "1006",
        "Calm rock": "1005",
        "Guitar songs": "1003",
        "Hard Rock": "1002",
        "Vals": "1001",
        "Milonga": "1000"
    }
    bards = set([
        "Чароит", "Владимир Высоцкий", 
        "Александр Городницкий", "Булат Окуджава", "Юрий Кукин",
        "Валерий Чечет", "Виктор Берковский", "Юрий Визбор", 
        "Пётр Налич, Иван Жук", "Дуэт “Русские Гитары”"
    ])
    punk_rock = set([
        "Sum 41"
    ])
    guitar = set([
        "КИНО", "Порнофильмы", "Сплин", "Ногу свело!", "Звери", "Пикник", "Nautilus Pompilius", 
        "Сектор Газа", "Василий Васильев", "Магелланово Облако", "Би-2", "Крематорий", "ЧайФ", 
        "Арктида", "Мумий Тролль", "ДДТ"
    ])
    russain_natural = ([
        "Пётр Лещенко", "Игорь Растеряев", "Сергей Лемешев", "Вадим Козин", "Фёдор Иванович Шаляпин", 
        "Олег Погудин", "Марина Ладынина"
    ])
    tracks_ids = list(map(lambda track: track["id"], client.users_likes_tracks().tracks))
    tracks = client.tracks(tracks_ids)
    artists = set()
    i = 55
    for track in tqdm(tracks, "Get tracks:"):
        artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
        if (artist in russain_natural):
            client.users_playlists_insert_track("1010", track["id"], track["albums"][0]["id"], revision = i)
            i+=1

def tracks_without_playlist(client):
    tracks_in_playlist = set()
    playlists = client.users_playlists_list()
    for playlist in playlists:
        for track in playlist.fetch_tracks():
            tracks_in_playlist.add(str(track.id))
    print (len(tracks_in_playlist))
    all_tracks = set(map(lambda track: track["id"], client.users_likes_tracks().tracks))
    print (len(all_tracks))
    tracks_out_playlist = all_tracks - tracks_in_playlist
    print (len(tracks_out_playlist))
    tracks = client.tracks(tracks_out_playlist)
    i = 1
    for track in tracks:
        artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
        print (artist + " - " + track.title.replace("/", "\\"))
        client.users_playlists_insert_track("1016", track["id"], track["albums"][0]["id"], revision = i)
        i+=1