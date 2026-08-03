---
name: log-bp
description: Record a new blood pressure reading in vault/Areas/Health/Blood Pressure.md - date/time, SYS/DIA/pulse, well-being note, comment. Use when Roman reports a blood pressure reading (text like "120/77, пульс 81", or a photo of the monitor), or explicitly asks to log/record his blood pressure.
---

# Log blood pressure

Log: `vault/Areas/Health/Blood Pressure.md`. This is data recording, not medical advice.

## Steps

1. Determine the date and time in Kyiv (`TZ=Europe/Kyiv date +"%F %H:%M"`).
2. Get SYS / DIA / Pulse:
   - As text (e.g. "120/77, пульс 81") — parse directly.
   - Photo of the monitor — read the screen. If any value is unclear/glare-obscured — **don't guess**.
     Clearly state what's visible and what isn't, and ask Roman to confirm what's missing.
3. Briefly ask about well-being if Roman didn't say himself — don't silently leave this field empty.
4. Add a new row at the bottom of the table in `vault/Areas/Health/Blood Pressure.md` (newest at
   the bottom, row format matching existing entries).
5. Commit and push to the session's active branch and `main`, as usual for vault files.

## What not to do

- Don't diagnose, don't explain symptom causes, don't give medical advice — recording only.
- If values look clearly atypical for Roman (very high/low) — briefly say so and suggest seeing a
  doctor, without analyzing "why" or reassuring.
- Don't invent missing values — if Roman didn't give well-being/comment, just ask.
