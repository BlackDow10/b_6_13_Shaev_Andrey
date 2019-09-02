from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album



@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
        result += "<br> Количество альбомов: {}".format(len(albums_list))
    return result

@route("/albums", method = "POST")
def save_data():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    print(album_data)
    session = album.connect_db()
    try:
        year = int(album_data["year"])
        if year < 1800 or year > 2019:
            raise ValueError
        if album.duble(album_data["artist"], album_data["album"]):
            raise Exception

    except ValueError:
        print("Введён неправильный формат даты")
    except Exception:
        print("Такой альбом уже существует")
        return HTTPError(407, "Такой альбом уже существует")
    else:
        album.reg(session, album_data)
        return "New album {} was saved successfully!".format(album_data["album"])
    
    


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)