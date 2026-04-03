# Custom Auth System (Django + DRF)

Проект реализует **собственную** систему аутентификации и авторизации (без использования встроенной Django auth как базы бизнес-логики).

## 1) Разделение ответственности

- **Аутентификация (кто пользователь?)**: register/login/logout, восстановление пользователя через `session_id` cookie.
- **Авторизация (что пользователю разрешено?)**: RBAC + правила действий на ресурсах.

## 2) Почему session-based

Основной поток сделан через серверные сессии в БД:
- проще и прозрачнее контролировать logout;
- легко инвалидировать доступ после soft-delete;
- наглядно видно, как middleware определяет пользователя в каждом запросе.

## 3) Схема БД

- `users` — кастомные пользователи (`is_active`, `is_deleted`, `deleted_at`, `password_hash`).
- `sessions` — серверные сессии (`session_key`, `expires_at`, `is_active`, ip/user-agent).
- `roles` — роли (`admin`, `manager`, `user`, `guest`).
- `user_roles` — many-to-many пользователь ↔ роль.
- `resources` — ресурсы (`users`, `products`, `orders`, `access_rules`).
- `access_rules` — права роли на ресурс:
  - `read_own/read_all`
  - `create_permission`
  - `update_own/update_all`
  - `delete_own/delete_all`

## 4) Логика 401 и 403

- **401 Unauthorized** — пользователь не определён (нет валидной сессии).
- **403 Forbidden** — пользователь определён, но не хватает прав.

## 5) Как работает middleware

`apps.core.middleware.CustomAuthMiddleware`:
1. читает cookie `session_id`;
2. ищет активную сессию и активного пользователя;
3. проверяет срок действия;
4. проставляет `request.user` и `request.session_obj`.

## 6) Soft delete

`DELETE /api/accounts/delete/`:
- `is_active=False`
- `is_deleted=True`
- `deleted_at=now`
- инвалидируются все активные сессии пользователя.

## 7) Endpoints

### Accounts
- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `POST /api/accounts/logout/`
- `GET /api/accounts/me/`
- `PATCH /api/accounts/me/`
- `DELETE /api/accounts/delete/`

### Access (admin only)
- `GET/POST /api/access/roles/`
- `GET/POST /api/access/resources/`
- `GET/POST /api/access/rules/`
- `GET/PATCH/DELETE /api/access/rules/{id}/`

### Business (mock)
- `GET/POST /api/business/products/`
- `PATCH/DELETE /api/business/products/{id}/`

## 8) Локальный запуск (Windows 10 + Git Bash)

```bash
python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## 9) Тестовые пользователи

После `seed_data`:
- `admin@example.com` / `Admin12345!`
- `user@example.com` / `User12345!`

## 10) Что важно на защите

- не используется `django.contrib.auth.User` для бизнес-логики;
- собственные таблицы пользователей и сессий;
- собственный middleware и проверка `request.user`;
- расширяемая RBAC-модель с own/all действиями.
