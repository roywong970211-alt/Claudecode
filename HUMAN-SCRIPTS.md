# Human Scripts — don't-sound-like-AI scripting for both IPs

This repo integrates the **StoryScope `human` skill** into your scriptwriting so nothing you publish sounds AI-generated. The research finding behind it: AI writing gives itself away by its *structure* (how a piece is built), not by em dashes or word choice. A classifier using structure alone told human from AI apart with 93.2% accuracy. So we fix the shape first, the surface second.

## What's here

```
.claude/skills/
  human/                 ← the base skill (the 9 structural principles + surface pass)
  human-nutritionist/    ← English, your nutrition/health IP
  human-qianjunwanma/    ← Chinese, your 千军万马 recruitment IP
```

Each persona skill loads the base `human` logic, then adds that IP's voice, format, and an AI-tell cleanup list (the Chinese one has its own, since em-dash rules don't map to Chinese).

## How to use it

**In Claude Code (this setup):** start a session in this repo and type:
- `/human-nutritionist write a 30s reel on magnesium and sleep`
- `/human-qianjunwanma 写一条招有带团队经验的人的短视频`
- `/human` for anything general, or `/human audit this` + paste text to just see what's wrong.

**In claude.ai / desktop:** the uploaded `human` skill works there already. To get the two persona skills there too, zip each folder (e.g. `human-nutritionist/`) into a `.skill` file and upload it under Customize → Skills. Or just paste the relevant `SKILL.md` into a chat as your instructions.

**Fastest, no setup:** paste a persona `SKILL.md` at the top of any chat, then your request.

## The 9 principles (quick reference)

1. Don't state the moral — cut the "and that's when I realized" ending.
2. Name feelings plainly — "she was scared," not "her chest tightened."
3. Be specific — real names, numbers, places, studies.
4. Talk to the reader — "you," direct, one person.
5. Don't tie a bow — leave some tension standing.
6. Let it wander a little — one connected side thread.
7. Play with time/order — start at the interesting moment, backfill.
8. Build tension that peaks — biggest moment near the end, vary the rhythm, cut the epilogue.
9. Pick the less obvious angle — the specific take only you would write.

Then a surface pass: no em dashes, no "it's not X it's Y," no AI vocab (delve, unlock, elevate, game-changer, "it's important to note").

> Note: the skill flags that Claude specifically tends to write flat tension, a uniform voice, and tacked-on epilogues — so these drafts are watched for exactly that.

Your own writing samples always override the defaults. Paste 2–3 of your real scripts and say "match my voice" and it will.
