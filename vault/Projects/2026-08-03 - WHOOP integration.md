---
tags: [projects]
date: 2026-08-03
---

# WHOOP integration (recovery/sleep/strain, не лише тренування)

Мета: дані з WHOOP (recovery, сон, strain) доступні асистенту широко — впливають на
`morning-checkin`/`evening-checkin`/`plan-day`/`workout`, а не лише на тренування.

## Чому не так просто, як з Hevy

WHOOP API — OAuth 2.0 з **токенами, що самі оновлюються** (rotating refresh tokens), не статичний
ключ. Тому патерн Base44/Hevy (env var + curl) не підходить — токен треба десь зберігати й оновлювати
з часом.

Правильний механізм — **Custom Connector через claude.ai** (Settings → Connectors → Add custom
connector, remote MCP по HTTPS). Це архітектурно інше від "сесія сама запускає MCP-сервер" (той
ризик з відсутністю сховища секретів у CCR, що вже задокументовано для custom MCP-серверів) — з'єднання
йде через хмару Anthropic, так само як уже підключені Google Drive/Slack/Notion.

Офіційного WHOOP-конектора в каталозі Anthropic немає → потрібен self-hosted реле-сервер. Роман уже
має Railway-акаунт (кілька особистих проєктів) → self-host, а не довіра чужому хостингу (це
біометричні дані здоров'я — вища чутливість, ніж просто лог тренувань).

**"Дім для різних сервісів"**: Роман хоче, щоб це був не одноразовий WHOOP-специфічний деплой, а
стандартний патерн для будь-якого майбутнього self-hosted особистого інтеграційного сервісу. Рішення:
**один Railway-проєкт "Personal Services"**, кожен сервіс всередині — окремий (WHOOP зараз, інші
потім), кожен зі своїм `claude.ai` custom connector. Не unified MCP-сервер з одним кодом на все —
Railway й так підтримує кілька сервісів в одному проєкті нативно, і кожен сервіс лишається окремим
upstream-проєктом (легше оновлювати, не наша інженерія). Задокументовано в `CLAUDE.md` як стандартний
патерн для наступних інтеграцій, не лише WHOOP.

## Обраний варіант: yuridivonis/whoop-mcp-server

https://github.com/yuridivonis/whoop-mcp-server — заточений саме під цей сценарій (remote HTTP MCP
сервер, задуманий як claude.ai custom connector), на **офіційному** WHOOP Developer API v2 (не
reverse-engineered приватний API, як-от `thebriangao/totem`, що менш стабільний і, ймовірно, порушує
ToS). Токени зберігаються в SQLite на Railway volume з авто-оновленням — проблема rotating tokens
вирішена всередині сервера.

MCP tools сервера: `get_today` (recovery+сон+strain, ранковий бриф), `get_recovery_trends`,
`get_sleep_analysis`, `get_strain_history`, `sync_data`, `get_auth_url`.

## Прогрес (оновлено 2026-08-04)

1. ✅ **Форк**: `github.com/Romms/whoop-mcp-server`, клоновано в `~/PersonalProjects/whoop-mcp-server`.
2. ✅ **Railway**: проєкт **"Personal Services"** (workspace "My Projects" на `rommssh@gmail.com` —
   не робочий `roman.shevchuk@uni.tech`, з тим спершу переплутали), сервіс задеплоєний, persistent
   volume на `/data` додано (SQLite тут переживе рестарти), домен
   `https://personal-services-production-dc3e.up.railway.app`.
3. ✅ **WHOOP Developer App**: створено, Client ID/Secret додані в Railway variables
   (`WHOOP_CLIENT_SECRET` — sealed, не видно навіть Роману після збереження — це нормально, сервіс
   його все одно бачить). Redirect URI, Privacy Policy (`/privacy` — мінімальна чесна сторінка,
   додана в код спеціально під вимогу форми), Contact — всі виставлені. `WHOOP_REDIRECT_URI`,
   `MCP_MODE=http`, `DB_PATH=/data/whoop.db` виставлені в Railway.
4. ✅ Redeploy з реальними креденшелами пройшов: `/health` → `{"status":"ok","authenticated":false}`
   (очікувано — авторизація ще попереду).
5. ✅ **Claude.ai custom connector**: додано, назва **"Whoop"**, tools (`get_today`, `get_auth_url`,
   `get_recovery_trends`, `get_sleep_analysis`, `get_strain_history`, `sync_data`) видно в сесії.
6. ✅ **Авторизація**: пройдена 2026-08-04 — `get_today` повертає реальні дані (recovery 56% Yellow,
   HRV 34.3ms, сон 8г22хв/91% performance, strain 4.0 Light), не auth error.

Лишається: 7) перевірити, що токен переживає рестарт Railway-сервісу (volume мав це вирішити, ще не
перевірено на практиці) 8) підключити дані у `morning-checkin`/`evening-checkin`/`plan-day`/`workout`.

## Безпека `/mcp` (додано 2026-08-04)

Роман запитав, чи MCP доступний лише йому — виявилось, `/mcp` не мав жодної автентифікації (форк
без цього). Виправлено:

- Bearer-токен на `/mcp` (`MCP_AUTH_TOKEN` env var у Railway, випадковий 32-байтний hex).
  `/health`, `/privacy`, `/callback` лишаються відкритими навмисно (перший два — публічний контент
  без чутливих даних, callback має спрацьовувати з WHOOP-редіректу без кастомних headers).
- **Важливий нюанс**: claude.ai **web**-інтерфейс для custom connectors має задокументовані баги зі
  static header/bearer auth (Anthropic issue tracker — налаштований header іноді не надсилається,
  замість цього стартує зайвий OAuth flow). Токен у URL — прямо заборонено специфікацією MCP. Тобто
  цей bearer-токен надійно захищає виклики з Claude Code/Desktop (там headers підтримуються
  коректно), але для claude.ai web/mobile може не спрацювати стабільно — тоді основний захист це
  непублікований/невідомий стороннім URL, а не сам токен.
- Заразом виправлено попередню (не мою) помилку у форку: `transport.handleRequest(req, res)` не
  передавав вже розпарсений `express.json()` body → "stream is not readable" на кожен виклик `/mcp`.
  Треба `transport.handleRequest(req, res, req.body)` — задокументовано навіть у самому SDK.
- Прибрано email Романа з публічної `/privacy` сторінки (не потрібен там — WHOOP-форма має власне
  поле Contact окремо).

Перевірено: без токена/з неправильним → 401; з правильним токеном → 200 і коректна MCP-відповідь.

**Оновлення того ж дня**: bearer-токен виявився несумісним із claude.ai web-конектором на практиці,
не лише теоретично — форма "Add custom connector" там взагалі не має поля для header/bearer, лише
OAuth Client ID/Secret (опційно). З токеном на `/mcp` конектор не міг "зареєструватись" (claude.ai
намагається достукатись без жодних headers, отримує 401 від нашого gate, і показує помилку
реєстрації). Роман сам прибрав `MCP_AUTH_TOKEN` з Railway variables — після цього конектор одразу
підключився, всі 6 tools видно (`get_auth_url`, `get_recovery_trends`, `get_sleep_analysis`,
`get_strain_history`, `get_today`, `sync_data`).

**Прийнятий компроміс**: `/mcp` зараз без автентифікації — захист лише через непублікований URL.
Код gate лишається в репо (вмикається знову, якщо колись `MCP_AUTH_TOKEN` виставити) — корисно, якщо
колись підключати цей самий сервер напряму з Claude Code/Desktop (там headers працюють), не через
claude.ai web. Побудова повноцінного власного OAuth-шару (щоб і безпечно, і сумісно з web-конектором)
— значно більший обсяг роботи, ніж уся решта інтеграції; не робили зараз, можна повернутись пізніше
як окрему Активні задачу, якщо це стане реальним пріоритетом.

Роман явно підтвердив 2026-08-04: "Лишаємо як є" — після прямого попередження, що будь-хто з цим URL
має доступ до реальних даних (не лише теоретично, свідомо прийнятий ризик, не недогляд).

## Що Клод підключає, щойно конектор живий

- `morning-checkin` — `get_today` поруч із наявним питанням про енергію/сон, не замість нього:
  показати дані, все одно запитати як відчувається — розбіжність (WHOOP каже низький recovery, а
  відчуття нормальні, чи навпаки) сама по собі варта уваги.
- `evening-checkin` — strain дня в existing fuel-guard питанні.
- `plan-day` — recovery впливає на амбітність дня (легший список / більші буфери), але завжди як
  озвучена пропозиція на підтвердження, не мовчазне коригування.
- `workout` — recovery/strain у пропозиції прогресії поруч із Hevy-історією (не заміна).
- `vault/Areas/Health/README.md` — WHOOP як джерело даних, dormancy-check отримує ще один пункт.

## Верифікація

1. `/health` на Railway відповідає OK.
2. `get_auth_url` → OAuth пройдено → `get_today`/`sync_data` повертає реальні дані, не auth error.
3. Рестарт Railway-сервісу (чи просто наступного дня) → `get_today` знову працює без re-auth —
   підтверджує, що токен переживає рестарт (сенс volume з кроку 3 вище).
4. Реальний прогін `morning-checkin` — recovery/сон читаються природно поруч з existing питанням.
