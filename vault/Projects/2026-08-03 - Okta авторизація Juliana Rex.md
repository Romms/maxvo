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

Запитано робочого асистента (Base44) розібратись, як зараз працює авторизація в Juliana та Rex (код,
Terraform, Okta/Auth0 конфіг) і чого саме бракує. Відповідь ще не отримана (запит виконується довго,
у фоні) — допишу сюди, коли прийде.

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

### Висновок (попередній, до відповіді робочого асистента)

Якщо Juliana/Rex — звичайні застосунки (як MCP, tRPC), то шлях через **Auth0** — вже існуючий,
перевірений патерн, і обходить блокер з API Access Management (не треба платного add-on / super
admin прав на Okta-орзі). Якщо ж їм справді потрібна саме пряма Okta-валідація (наприклад,
server-to-server без посередника, чи специфічні access policies на рівні Okta), тоді потрібно
розблоковувати API Access Management у Okta-орзі.

Остаточне рішення — після відповіді робочого асистента про реальний поточний стан Juliana/Rex.
