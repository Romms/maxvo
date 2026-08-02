---
name: plan-day
description: Time-block today's (or a named day's) tasks into Roman's dedicated "Daily Tasks" Google Calendar - brain dump, prioritize/size, then fill the calendar around fixed commitments with realistic buffers. Also re-plans the rest of the day if something runs over. Use when Roman asks to plan his day, block out his day, "розплануй день", "заповни календар задачами", or invokes /plan-day. Do NOT use this for the lightweight morning-checkin ritual (single priority + first step) unless he explicitly asks for the fuller planning session this time.
---

# Планування дня: brain dump → пріоритет → блоки в календарі

Roman's own method (short list → priority per item → add to calendar one by one until the day fills
up), combined with evidence-based adjustments: time blocking works especially well for ADHD because
it does prioritization once instead of re-deciding all day, but naive time blocking fails without
buffer time — ADHD time-estimates run optimistic, so blocks need slack built in.

## Календар

Задачі-блоки йдуть в окремий календар **"Daily Tasks"**, не на основний/Appointments — щоб не
змішувати з реальними зустрічами. Резолви `calendarId` через `list_calendars` за назвою "Daily Tasks"
(не хардкодь ID — календар могли перестворити).

## Крок 1: brain dump

Зібрати список задач на день:
- Запитати прямо: "які задачі на сьогодні?"
- Підмішати з `vault/Projects/README.md` Активні те, що має дедлайн сьогодні/цього тижня
- Глянути `vault/Inbox.md` Unprocessed на щось схоже на задачу на сьогодні

Просто зібрати список, коротко — не обговорювати і не пріоритизувати на цьому кроці.

## Крок 2: пріоритет і розмір

Для кожної задачі — пріоритет і грубий розмір (T-shirt: маленька ~15-20 хв / середня ~30-45 хв /
велика ~60-90 хв).

Якщо задач забагато для одного дня (орієнтовно >9, або сума оцінок явно не влазить у робоче вікно) —
не мовчки урізати список. Сказати вголос і застосувати м'який ліміт: 1-3-5 (1 велика + 3 середні +
5 дрібних) або Ivy Lee (не більше 6, суворий пріоритетний порядок, наступне не починається поки не
закрите попереднє). Питання одне: "Це забагато для сьогодні. Що з цього реально мусить бути зроблено
сьогодні?" — решта в `vault/Projects/README.md` Активні (не втрачається, просто не сьогодні).

## Крок 3: фіксовані зустрічі

`list_events` на реальних календарях Романа (основний `rommssh@gmail.com`, `Appointments`) на
потрібний день — не на "Daily Tasks", там лише блоки задач. Зустрічі — анкери, блоки задач будуються
навколо них, не поверх.

Якщо робоче вікно дня не очевидне — запитати ("з якої до якої сьогодні працюємо?"), інакше
запропонувати дефолт 09:00–19:00 і озвучити його, а не мовчки припустити.

## Крок 4: заповнення календаря

По черзі, у пріоритетному порядку:
- Тривалість блоку = оцінка розміру + ~25% буфер (корекція на ADHD-недооцінку часу)
- 10-15 хв між блоками на перемикання — не впритул один до одного
- Обходити фіксовані зустрічі, не перекривати їх

Перед тим як реально створювати events — показати Роману запропонований розклад одним повідомленням
(час → задача, по порядку), дати шанс швидко поправити порядок/тривалість. Тільки після цього
створювати events через `create_event` на "Daily Tasks" (`summary` = коротка назва задачі).

Для середніх/великих задач — розбити її на короткий ланцюжок конкретних кроків (як в
morning-checkin, див. "Task breakdown" в `docs/daily-rituals.md`) і покласти в `description` event'у,
не тільки назву. Мета та сама: не дати застрягнути на "що далі" всередині блоку.

## Виконання протягом дня: replan

Коли Роман каже щось на кшталт "затягнулось", "переплануй решту дня", "не встигаю" — без довгих
розпитувань: подивитись поточний час і які блоки на "Daily Tasks" ще попереду сьогодні, коротко
запитати що з поточної задачі ще актуальне, і зсунути решту блоків від (поточний час + буфер) в тому
ж пріоритетному порядку. Оновлювати наявні events (`update_event`), не створювати дублікати.

## Після дня

Завершення дня — робота `evening-checkin` (`vault/Daily/YYYY-MM-DD.md` `## Вечір`), тут це не
дублювати. Якщо після replan щось відпало з дня зовсім — воно йде в `vault/Projects/README.md`
Активні або `vault/Inbox.md` як зазвичай, не губиться мовчки.
