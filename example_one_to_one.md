## Пример реализации связи "один к одному" в базе данных на примере сущностей Пользователь (User) и Профиль (Profile)
### 1. Создание таблиц

```sql
-- Таблица пользователей
CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица профилей
CREATE TABLE Profiles (
    user_id INT PRIMARY KEY, -- Связь 1:1 через первичный ключ
    birth_date DATE,
    avatar_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);
```

**Users**: хранит основные данные пользователя.

**Profiles**: хранит дополнительные данные, связанные ровно с одним пользователем.

user_id в таблице Profiles является:

* **Первичным ключом** (не может повторяться).
* **Внешним ключом** (ссылается на Users.id).
* ON DELETE CASCADE: при удалении пользователя автоматически удаляется его профиль.

### 2. Вставка данных
```sql
-- Создаем пользователя
INSERT INTO Users (username, email) 
VALUES ('alex', 'alex@example.com');

-- Создаем профиль для пользователя с id=1
INSERT INTO Profiles (user_id, birth_date, avatar_url) 
VALUES (1, '1990-05-15', 'https://example.com/avatar.jpg');
```

### 3. Выборка данных
**Запрос с использованием** INNER JOIN:

```sql
SELECT Users.username, Profiles.birth_date 
FROM Users
INNER JOIN Profiles ON Users.id = Profiles.user_id;
```

**Результат:**

```cmd
username | birth_date
---------------------
alex     | 1990-05-15
```

### 4. Пример реализации через ORM (Python, SQLAlchemy)
```python
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100), unique=True)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = 'profiles'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    birth_date = Column(Date)
    avatar_url = Column(String(255))
    user = relationship("User", back_populates="profile")
```

* **uselist=False** указывает, что связь один к одному (по умолчанию — один ко многим)

### 5. Когда использовать связь 1:1?
* Разделение часто/редко используемых данных (оптимизация запросов).
* Изоляция конфиденциальных данных (например, паспортные данные в отдельной таблице).
* Избежание избыточности NULL-значений, если часть данных не обязательна

### 6. Важные нюансы
* Уникальность связи гарантируется первичным ключом в таблице **Profiles**.
* Каскадное удаление (**ON DELETE CASCADE**) обеспечивает целостность данных.
