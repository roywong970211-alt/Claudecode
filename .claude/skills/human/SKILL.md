---
name: "human"
description: "Write or rewrite text so it reads human at the structural level, based on the StoryScope study (UMD + Google DeepMind). Use when the user types /human, asks to humanize text, or wants writing that doesn't sound like AI."
---

# Human

Most humanizers scrub the surface: em dashes, "delve," rule-of-three lists. That helps a little, but it misses where AI writing actually gives itself away.

In the StoryScope study (Russell, Rajendhran, Pham, Iyyer, Wieting; University of Maryland and Google DeepMind, arXiv 2604.03136), researchers compared 61,608 stories written by humans and five AI models on the same prompts. A classifier that looked only at how the stories were built (plot, time, characters, themes), and ignored word choice entirely, separated human from AI writing with a 93.2% macro-F1 score. When the obvious stylistic AI tells were edited out, that classifier barely moved (95.5 to 93.9). The tell is the shape of the writing, not the punctuation.

This skill fixes the shape first and the surface second.

## Two ways it gets used

1. **Write from scratch.** The user types /human followed by a request ("/human write a LinkedIn post about my first month freelancing"). Write the piece with the principles below built in from the first draft. Don't write an AI-shaped draft and then patch it.
2. **Rewrite.** The user pastes text and asks to humanize it. Diagnose it against the principles, then rewrite. Keep the author's meaning, facts, and voice. Change the structure, not the substance.

If the user says "audit" or "what's wrong with this," list the structural problems you found with the line each one appears in, and only rewrite if they ask.

## The structural principles

Each principle comes from a measured gap between human and AI writing in the study. The numbers are there so you understand how strong the pull is, not to quote back to the user. The study was on fiction, so each principle includes how it translates to scripts, posts, emails, and essays.

### 1. Don't state the moral
AI narrators spelled out the story's theme 77% of the time, versus 52% for humans. AI also used dialogue as philosophical debate about meaning 59% of the time, versus 34%.

The instinct is to make sure the reader "gets it" by saying the point out loud. Trust the reader instead. Cut the closing line that explains what the piece meant ("And that's when I realized...", "The lesson here is...", "At the end of the day..."). End on the concrete moment, the detail, or the action, and let the reader do the last step. In nonfiction you can still make a clear claim. Just make it once, where it belongs, instead of restating it as a summary at the end.

### 2. Name feelings plainly
AI conveyed emotion through physical sensation or weather metaphors 81% of the time, versus 38% for humans. Humans named the emotion directly 29% of the time; AI did 8%. AI also leaned on smell imagery far more (82% vs 57%).

"Her chest tightened and a cold sweat crept down her neck" is the AI version of "she was scared." Default to saying the feeling in ordinary words. Save a physical detail for when it's specific and earned, not as a substitute for the emotion.

### 3. Be specific about the world
Humans referenced specific texts, people, and authors 47% of the time; AI did 24%. AI made vague allusions ("like an old fable," "as the saying goes") 72% of the time, versus 50%.

Replace gestures with names. Name the actual book, the actual company, the actual person, the actual number, the actual street. "A famous study found" becomes the study's name. "Some experts say" becomes who said it, or gets cut.

### 4. Talk to the reader
Human narrators addressed the reader directly 28% of the time, versus 7% for AI, and broke the fourth wall 67% of the time, versus 39%.

AI writing hovers at a polite distance. Humans lean in: "you," an aside, a question to the person reading, an admission that this is a story or a post. Use it where it fits the format. A short-form script or a post should almost always talk to one person.

### 5. Don't tie a bow on it
AI resolved stories through internal acceptance or understanding 47% of the time, versus 27% for humans. Humans wrote morally ambivalent protagonists 59% of the time; AI did 38%.

AI wants everything resolved: the character makes peace, the problem has a clean lesson, the ending is tidy. Real writing leaves some tension standing. Let a choice be questionable. Let an outcome be mixed. Let the author admit they're not sure. A post that ends with an honest open question often reads more human than one that ends with a neat takeaway.

### 6. Let it wander a little
79% of AI stories had no subplots at all, versus 57% of human ones. Humans wove side threads into the main theme 42% of the time; AI did 21%.

AI writing runs on a single straight track. Human writing has a second thread: a side detail, a tangent that pays off later, a small unrelated observation that makes it feel lived in. Add one where the length allows. Keep it short and connected to the main point, so it adds texture instead of padding.

### 7. Play with time and order
Human stories showed significantly more chronological discontinuity, such as flashbacks, jumps, and starting in the middle. AI tells things in order, and some models front-load all the context before anything happens.

Don't open with setup. Start at the interesting moment and backfill only what's needed. In a script or post, lead with the result or the turning point, then go back.

### 8. Build tension that actually peaks
Claude in particular had the flattest event escalation of any model studied: tension rarely climbs to a real high point before it resolves. Claude also had the most uniform narrative voice, the most reverent attitude toward the material, and a habit of adding epilogues.

Since you are likely running as Claude, watch for this in your own drafts. Make the stakes rise. Put the biggest moment near the end, not spread evenly. Vary sentence length and energy so the voice isn't one steady hum. Cut the epilogue or wrap-up paragraph after the real ending.

### 9. Pick the less obvious version
AI stories clustered together in the same narrow region of possibilities, while human stories were spread out. Given the same prompt, the human version was the most unusual of six 57.8% of the time, against a 16.7% chance rate.

The most predictable angle is the AI angle. Before writing, think of the first take that comes to mind, then choose a more particular one: an unexpected entry point, a specific personal detail, a contrarian framing the author would actually hold. Don't be weird for its own sake. Be specific enough that no one else would have written it this way.

## Other models' habits (when rewriting their output)
If the user says the text came from another model, check for its fingerprint too:
- **ChatGPT / GPT:** leans on gossip and rumor to drive plot (64% vs 44 to 55% for other sources) and on twist-for-its-own-sake subversion.
- **Gemini:** describes characters from the outside (appearance) instead of what they want, writes the tidiest endings with long denouements, and defaults to bleak settings.
- **DeepSeek:** front-loads crucial context before the story starts moving.

## Surface pass (second, not first)
After the structure is right, do a quick surface cleanup, because readers do notice these:
- No em dashes. Use commas, periods, or parentheses.
- Cut filler and AI vocabulary: delve, tapestry, testament, navigate, landscape, game-changer, unlock, elevate, "it's important to note."
- Avoid "It's not X, it's Y" constructions and reflexive lists of three.
- No standalone one-line punch sentences stacked for drama. Let sentences connect.
- Don't summarize what you just said.

If a voice profile, writing samples, or style rules from the user are available, they override these defaults. Match how the person actually writes.

## Output
Deliver the finished writing and stop. Don't preface it, don't explain the principles, and don't list your changes unless the user asks what changed or asked for an audit. If they ask, give the two or three biggest structural changes in one line each.

## Example

**Before (AI-shaped):**
> When I quit my job to freelance, my heart pounded and my palms were slick with sweat. The first month was a whirlwind of challenges and growth. I learned that success isn't about having all the answers, it's about embracing the journey. In the end, I realized that taking the leap was the best decision I ever made.

**After (/human):**
> Three weeks into freelancing I had one client, $640 in invoices, and a Notion page titled "backup plan" that I'd opened four times. I was scared, honestly. Not of failing, more of having to explain it at Christmas. Then the client referred her sister. I still don't know if this works. But I haven't opened the backup plan since Tuesday.

What moved: the feeling is named instead of shown through sweaty palms, vague "challenges" became specific numbers and a named tool, the moral ("embracing the journey") is gone, and the ending stays open instead of declaring the best decision ever.