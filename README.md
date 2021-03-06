# Ticket system REST API
## Общее описание
Регистрацию, авторизация и аутентификация отсутствует, предполагается, что
запросы приходят от известного пользователя.
Реализация на Python 3.9.1, также используются Flask, PostgreSQL, SQLAlchemy, uWSGI, Redis (версии в requirements.txt)
Только API (пользовательские интерфейсы отсутствуют).

##### Тикет-система состоит из:
- Тикетов, у тикетов могут быть комментарии
- Тикет создается в статусе “открыт”, может перейти в “отвечен” или “закрыт”, из
отвечен в “ожидает ответа” или “закрыт”, статус “закрыт” финальный (нельзя
изменить статус или добавить комментарий).
Все статусы:
  - открыт
  - отвечен
  - ожидает ответа
  - закрыт

##### Тикет имеет свойства:
- ID
- Дата создания
- Дата изменения
- Тема
- Текст
- Email
- Статус

##### Комментарий имеет свойства:
- ID
- ID тикета
- Дата создания
- Email
- Текст



## REST API методы:
1. Создание тикета POST /api/tickets
2. Изменить статус PUT /api/tickets/<id тикета>/
3. Добавить комментарий PUT /api/tickets/<id тикета>/
4. Получить тикет GET /api/tickets/<id тикета>/
