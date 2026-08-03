---
tags: [project, work]
---

# Okta авторизація для Juliana та Rex

Руслану треба переробити авторизацію для проєктів **Juliana** та **Rex**. (Попередній запис в
Активні мав помилку — "VS" був одруком, правильно — Juliana/Rex.) Пов'язана заблокована задача з
Notion: **"Switch on Okta Direct Auth when API Access Management is enabled for our org"** (Assignee:
Ruslan Kobieliev, Blocked).

Два паралельні потоки дослідження (03.08):

## Потік 1: робочий асистент — поточний стан Juliana/Rex

### Juliana (`apps/api` + `apps/web`)

Browser → Okta (PKCE) → Okta access token → Juliana API (JWKS validation). Локальні ролі
(`UserRole { User, Admin, OpsAdmin }`, `RexUserAccessGuard`) — не з Okta.

- В продакшені зараз працює в **legacy mode** (`OKTA_DIRECT_JWT=false`): API сам мінить JWT pair,
  confidential Okta flow (authorization code + client_secret) — старий, "мертвий" в сенсі напрямку
  розвитку код (`okta.service.ts`).
- Plan 108 (перехід на direct Okta PKCE) **уже повністю реалізовано в коді**, просто не увімкнений.

### Rex (`apps/rex-api`)

Та ж модель (Bearer Okta token → JWKS validation), але **окремий deployment**, власна БД, власний
auth-модуль (не спільний пакет із Juliana). **Без legacy fallback** — вимагає direct Okta, і без
нього продакшн не працює. **Auth0 не використовує взагалі.** M2M між Rex і Juliana — окремо, через
HMAC-signed HTTP, не Okta.

### Auth0 — де він реально є (і де немає)

**Auth0 не використовується ні для Juliana, ні для Rex.** Auth0 керує MCP Clients (Claude/Cursor),
scribe-mcp, decisions-mcp, okta-automations, unicore-railway.io — окремий домен застосунків.

### Головний блокер (задокументований, decision `D-20260721-direct-okta-ready-pending-api-access-management`)

**Okta API Access Management не увімкнений на `universe.okta.com`.** Custom authorization server
повертає `E0000015` ("немає прав на цю фічу"). Org authorization server працює, але не підходить:
його токени не містять `email` claim, потрібний `OktaUserResolver`-у, і Okta не підтримує валідацію
org-server токенів на стороні resource server. **Це платний Okta add-on — ops/licensing рішення, не
код.**

Через це: Juliana сидить у legacy-режимі, а Rex-api — повністю готовий код, але "dark by config only"
(не може піти в прод через той самий блокер + окремо потребує Phase 4 інфраструктури: subdomain,
Doppler project, Okta-конфіг).

### Висновок робочого асистента щодо Okta vs Auth0

**Перехід Juliana/Rex на Auth0 був би кроком назад**, не рішенням: Auth0 федерується через Okta, але
валідація на resource-server все одно лишається на боці застосунку — тобто той самий блокер
(API Access Management) нікуди не зникає, а весь auth-модуль довелось би переписувати заново.

## Потік 2: Клод — Okta-концепти й порівняння з Auth0

### API Access Management (Okta)

Платний add-on до Okta org (потрібен саме для того, що заблокувало Руслана). Це "OAuth-as-a-Service":
дозволяє створювати **Custom Authorization Servers** — по суті, окремий "OAuth 2.0 token minting
engine" з власним issuer URI та ключем підпису. Без цього add-on доступний лише вбудований **Org
Authorization Server** — не кастомізується, дає широкий, але фіксований набір claims/scopes.

Custom Authorization Server потрібен, коли:
- ви самі захищаєте власні API (не просто логін користувачів);
- потрібен тонкий контроль над вмістом токена (свої scopes, claims);
- потрібні різні access policies для різних груп користувачів/застосунків;
- застосунок сам валідує токен (а не покладається на посередника).

([Okta Developer — API Access Management](https://developer.okta.com/docs/concepts/api-access-management/),
[Okta Authorization Servers — Cloudworks](https://www.cloudworks.no/en/articles/okta-authorization-servers))

### Okta Direct Authentication (Direct Auth)

Набір auth API, де застосунок сам збирає credentials користувача і напряму звертається до Okta
`/token` endpoint — без редиректу через браузер на IdP (тобто без стандартного OIDC
authorization-code флоу через посередника типу Auth0). Використовується, коли застосунок хоче сам
керувати UX верифікації факторів, а не делегувати його IdP.

**Ключове**: Direct Auth спирається на OAuth 2.0 токени й authorization servers, тому **вимагає API
Access Management** як prerequisite (звідси й назва заблокованої задачі Руслана — "Switch on Okta
Direct Auth when API Access Management is enabled"). Ввімкнення також вимагає прав super admin.

([Okta Developer — Direct Authentication](https://developer.okta.com/docs/concepts/direct-authentication/),
[Configure Direct Authentication](https://developer.okta.com/docs/guides/configure-direct-auth-grants/aotp/main/))

### Що з цього вже покриває Auth0

Ваш поточний стек (з відповіді робочого асистента раніше) уже поєднує обидва:
**Okta (IdP, логін користувачів) → Auth0 (app-level OAuth/OIDC шар) → застосунки/сервіси**. Auth0 вже
інжектить Okta groups у токени через post-login Action — задеплоєно й працює для MCP APIs та tRPC.

Порівняння підходів до кастомних claims/груп:
- **Okta** (custom authorization server): claims/groups налаштовуються в конфігурації самого
  authorization server-а (для org authorization server — на sign-on tab застосунку; для custom — у
  налаштуваннях самого сервера).
- **Auth0**: через **Actions** — код на Node.js, що вбудовується у flow логіну й додає власний claim
  у токен. У вашому випадку це вже і є той механізм, що інжектить Okta groups.

Загальна оцінка з пошуку: Auth0 дає гнучкіший рівень кастомізації (Actions/Hooks/Rules) порівняно з
Okta-native кастомізацією.

([Auth0 vs Okta — StackShare](https://stackshare.io/stackups/auth0-vs-okta),
[Customize tokens with custom claims — Okta Developer](https://developer.okta.com/docs/guides/customize-tokens-returned-from-okta/main/))

### Висновок

Попередня гіпотеза (нижче, закреслена по суті) припускала, що Auth0 міг би обійти блокер — **це
виявилось невірно**. Juliana/Rex вже архітектурно на direct Okta (не Auth0), і Auth0 не вирішує сам
блокер (валідація токена все одно на стороні застосунку). Перехід на Auth0 = переписати весь
auth-модуль заради нуля вигоди.

**Реальний наступний крок:** увімкнути Okta API Access Management на `universe.okta.com` — це
ops/licensing рішення (можливо платний add-on, потрібні права super admin на Okta-орзі), не задача
для коду. Після цього — прапорці в Doppler (`OKTA_DIRECT_JWT=true` для Juliana) і, окремо для Rex —
Phase 4 інфраструктура (subdomain, Doppler project, Okta-конфіг).

<details><summary>Попередня (спростована) гіпотеза, для історії</summary>

Якщо Juliana/Rex — звичайні застосунки (як MCP, tRPC), то шлях через Auth0 — вже існуючий, перевірений
патерн, і обходить блокер з API Access Management. Якщо ж їм справді потрібна саме пряма
Okta-валідація, тоді потрібно розблоковувати API Access Management у Okta-орзі.

</details>

## Перегляд висновку (03.08, після прайс-листа)

Роман показав прайс-лист поточної Okta-підписки (36 місяців, оплата раз на 3 роки): **Okta Single
Sign-On, Universal Directory, Multi-factor, Lifecycle Management, EU Hosted Cell**. **API Access
Management в списку немає** — тобто це в будь-якому разі нова покупка, не розширення наявного плану.
Роман: готовий переписати все, якщо треба; якщо потрібне щось нове — за інших рівних вважає за краще
Auth0, якщо там та сама функціональність.

Це справедливо ставить під сумнів попередній висновок "Auth0 не рішення": та відповідь порівнювала
"Auth0 як додатковий шар поверх Okta custom auth server" (справді безглуздо), а не "Auth0 як **заміна**
ролі authorization server-а" — тобто Okta лишається лише SSO/IdP (те, що вже й так оплачено), а Auth0
мінить access-токени з потрібними claims (email, audience) через Actions — точно той самий патерн,
що вже задеплоєний і працює для MCP-тулів. Це технічно інша конфігурація, не "крок назад" — вимагає
лише переточити `OktaJwtStrategy`/JWKS-валідацію в Juliana й Rex на issuer Auth0 замість Okta.

Питання, яке лишилось відкритим і варте окремого запиту робочому асистенту: скільки реально коштує
Okta API Access Management add-on (чи є ця цифра десь у контрактах/перемовинах) — щоб порівняти з
інкрементальною вартістю Auth0 для двох додаткових застосунків.
