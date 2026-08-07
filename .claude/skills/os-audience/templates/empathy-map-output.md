# Empathy Map — canonical output shape

Use this shape for `modes/empathy-map`. Compact output — the empathy map is a quick zoom onto a specific audience-moment, not a full psychographic profile.

## Shape

```markdown
# Empathy Map: [Target Audience] — [Context or Moment]

1. **Thinks** — [internal thoughts the audience is having in this moment. What's running through their mind?]
2. **Feels** — [emotions. Named specifically — not "bad" but "quietly ashamed," "restless," "smug," "relieved."]
3. **Says** — [what they'd say out loud in this context. Voice matters — it's often filtered, defensive, or performative compared to what they think.]
4. **Does** — [observable behavior. Actions, habits, tell-tale movements.]
5. **Sees** — [what's in their visual environment — interfaces, people, places, feeds. What's competing for their attention.]
6. **Hears** — [what they're listening to — voices around them, media they consume, messages from peers/authority figures.]
7. **Pains** — [frustrations, blockers, unmet needs felt in this moment.]
8. **Goals** — [what they hope to achieve — short-term immediate, not long-term life goals.]
```

## Key rules

- **Format: numbered list, bold category words.** As specified in source.
- **Bind the empathy map to a context.** An empathy map for "a coach" is too broad. An empathy map for "a coach on a Sunday night preparing Monday's sessions" is usable. Ask for a specific moment if the input doesn't give one.
- **Named emotions, not generic ones.** *"Bad"* / *"frustrated"* are thin. *"Quietly ashamed of the undelivered course outline"* / *"restless because the side hustle hasn't broken through yet"* are thick. Specificity matters.
- **Distinguish between Says and Thinks.** If they're the same, you're missing the filter. What people say is usually performance-adjusted. What they think is closer to the truth.
- **Sees and Hears are environmental, not internal.** They're the signal-noise the prospect is swimming in. Social feeds, overheard conversations, advisor voices, ambient media.
- **Pains and Goals are situational, not life-level.** Empathy maps profile moments, not life arcs. Life-level material goes in `modes/avatar`.

## When to use the table variant

If the user prefers structured output (e.g., to paste into a slide or spreadsheet), use a two-column table:

```markdown
| Category | Content |
|----------|---------|
| Thinks | ... |
| Feels | ... |
| Says | ... |
| Does | ... |
| Sees | ... |
| Hears | ... |
| Pains | ... |
| Goals | ... |
```

Default is the numbered-list format.

## What this template is not

- Not a substitute for avatar analysis. Empathy maps are narrower and moment-bound.
- Not a demographic profile.
- Not content ideas or messaging recommendations.
