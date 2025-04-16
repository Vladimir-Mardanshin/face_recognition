**Настройка окружений для QMagFace и Qdrant Server**

1. **Открываем QMagFace в PyCharm**

- Откройте проект QMagFace в PyCharm.  
- Убедитесь, что в корне проекта находится файл `environment.yml`.  
- Создайте окружение Conda с помощью команды:

  ```
  conda env create -f environment.yml
  ```

  Это установит все зависимости, указанные в `environment.yml`, и создаст окружение с нужной конфигурацией.

2. **Скачивание и размещение данных для QMagFace**

- Скачайте заранее подготовленные эмбеддинги MagFace и файлы пар по [этой ссылке](https://drive.google.com/file/d/1ElwkUKFs6-4JEwRnsKh6fJLp00x_FOvS/view) и распакуйте их в корневую директорию проекта `QMagFace`.

- Скачайте модель MagFace100 по [этой ссылке](https://drive.google.com/file/d/1Bd87admxOZvbIOAyTkGEntsEz3fyMt7H/view) и поместите её в директорию `_models/magface_models/`.

  Структура каталогов должна выглядеть примерно так:

  ```
  QMagFace
      _data
          ijb
          pairs
          single_images
      _models
          magface_models
              magface_epoch_00025.pth
          mtcnn-model
      datasets
      ...
  ```

---

3. **Открываем qdrant_server**

- Откройте проект qdrant_server в PyCharm.  
- Убедитесь, что активировано нужное Python-окружение.  
- Установите необходимые зависимости:

  ```
  pip install qdrant_client flask flask-cors
  ```

  Эти библиотеки необходимы для запуска сервера и взаимодействия с Qdrant API.

---
