# dankert_download

![logo](https://raw.githubusercontent.com/Dan-Kert/dankert-download/refs/heads/main/devscripts/logo.ico)

## ⚡️ dankert_download — мощный загрузчик видео и аудио

Альтернатива yt-dlp, поддерживает десятки платформ: **TikTok, YouTube, Instagram, VK, Pinterest, Likee, SoundCloud, RuTube** и другие.

---

## 🔥 Возможности

- 🧠 Автоматическое распознавание ссылок с популярных платформ
- 📥 Скачивание видео, аудио, фото, gif
- 📝 Сохранение метаданных: автор, подпись, ID, описание
- 🏷️ Поддержка глав, аннотаций, спонсорских блоков
- 🗂️ Работа с плейлистами, каналами, профилями
- 🔒 Обход ограничений возраста и приватности
- 🌐 Кросс-платформенность: Windows, Linux, Termux (Android)
- 🧩 Плагины и расширения
- ⚙️ Гибкая настройка через конфиг и параметры командной строки
- 🚀 Высокая скорость загрузки, поддержка многопоточности

---

## 📦 Установка

```sh
pip install .
```

или для разработки:

```sh
pip install -e .
```

---

## 🚀 Быстрый старт

Скачайте видео по ссылке:

```sh
dankert_download "https://www.youtube.com/watch?v=ID"
```

Скачайте TikTok:

```sh
dankert_download "https://www.tiktok.com/@user/video/1234567890"
```

---

## ⚙️ Примеры использования

Скачать аудио:

```sh
dankert_download "https://soundcloud.com/artist/track"
```

Скачать плейлист:

```sh
dankert_download "https://www.youtube.com/playlist?list=PLxxxx"
```

Указать формат:

```sh
dankert_download "https://youtu.be/ID" --format mp4
```

---

## 🛠️ Параметры командной строки

- `--format` — выбрать формат (mp4, webm, mp3 и др.)
- `--output` — указать имя файла или папку
- `--proxy` — использовать прокси
- `--info` — вывести информацию о видео
- `--no-merge` — не объединять аудио и видео
- `--config` — использовать свой конфиг

Полный список параметров смотрите через:

```sh
dankert_download --help
```

---

## 🧩 Расширения и плагины

- Поддержка пользовательских плагинов
- Примеры в папке `plugins/`
- Документация по API для расширения функционала

---

## 🧪 Тесты

Запуск тестов:

```sh
pytest test
```

---

## 📝 Документация

- [Wiki](https://github.com/Dan-Kert/dankert-download/wiki)
- [FAQ](https://github.com/Dan-Kert/dankert-download/wiki/FAQ)
- [Список поддерживаемых платформ](https://github.com/Dan-Kert/dankert-download/wiki/Platforms)

---

## 💬 Обратная связь

- [GitHub Issues](https://github.com/Dan-Kert/dankert-download/issues)
- [Telegram](https://t.me/dankertbot)
- [Email](mailto:dan.kert.official@gmail.com)

---

## 📝 Лицензия

MIT License

---

## 👨‍💻 Автор

DanKert  
[GitHub](https://github.com/Dan-Kert)  
[Telegram](https://t.me/dankert)

---

## ⭐️ Поддержите проект!

Поставьте ⭐️ на GitHub, расскажите друзьям, присоединяйтесь к сообществу!
