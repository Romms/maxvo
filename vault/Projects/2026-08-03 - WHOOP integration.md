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

## Кроки (сторона Романа — інфраструктура/акаунти, Клод це зробити не може)

1. **WHOOP Developer App**: developer.whoop.com → створити застосунок → Client ID/Secret → redirect
   URI = майбутній `https://<app>.railway.app/callback`.
2. **Форкнути репо** у свій GitHub (не деплоїти з чужого репо напряму).
3. **Railway**: якщо ще нема — створити проєкт **"Personal Services"** (дім для всіх майбутніх
   self-hosted особистих інтеграцій, не лише WHOOP) → додати новий **сервіс** всередині проєкту з
   форку whoop-mcp-server → env vars `WHOOP_CLIENT_ID`, `WHOOP_CLIENT_SECRET`, `WHOOP_REDIRECT_URI`
   → **persistent volume на `/data`** (тут живе SQLite з токенами — без цього доведеться re-auth
   після кожного рестарту) → deploy → перевірити `/health` цього сервісу.
4. **Claude.ai custom connector**: Settings → Connectors → Add custom connector → назва **"Whoop"**
   (впливає на передбачувану назву tools далі) → URL `https://<app>.railway.app/mcp`.
5. **Одноразова авторизація**: викликати `get_auth_url` у будь-якому чаті → перейти за посиланням →
   логін у WHOOP → авторизувати → редірект назад → стартує початкова синхронізація за 90 днів.

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
