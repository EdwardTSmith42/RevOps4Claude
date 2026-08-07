# Internet Writing Rules

Stated rules for prose written for online audiences. Loaded by `modes/humanize` to guide the rewritten output's surface form. Pairs with `../../_shared/references/ai-writing-patterns.md`: the AI-writing catalog is *what to remove*. These rules are *what to write toward*.

## The rules

### 1. Readability — line breaks aid scanning

Each post should include two markdown line breaks (`\n\n`) between most sentences so the reader can easily scan and understand the content. Online attention is fast and scrolling. Dense paragraphs lose readers.

Example structure:
```
{first line — a punchy one-liner}.

{another punchy one-liner}

{three super-short sentences in a row}

{the post continues...}
```

Rule of thumb: when in doubt, line break. Long unbroken paragraphs work in print and academic writing. They fail online.

### 2. Crisp writing — waste no words

Attention spans are short. Favor the simple tense of verbs ("write" not "writing"). Avoid purple prose. Use active voice most of the time, unless it doesn't make sense for what you're writing.

The rule isn't "be terse" — it's "don't waste words." A 2,000-word piece can be crisp if every word is doing work.

### 3. Why read this? Give them a reason

Readers subconsciously look for "what's in it for me?" Give it to them — early. The hook should answer it. The opening line should justify the read.

This connects to the specificity principle (see `editing-principles.md`): "why read it?" is one of the four questions every piece should answer.

### 4. No clickbait

People appreciate genuine, relatable content that delivers on its promises. Clickbait headlines that don't pay off lose readers permanently — the cost of one clickbait failure is many pieces of trust.

Promise what the piece actually delivers. Over-deliver if possible. Under-promise > clickbait > over-deliver, in that order.

### 5. Specificity is key

Specificity is key in good writing. Turn the vague into the specific.

- "Many businesses" → "Most B2B SaaS companies"
- "Get more opens" → "2x open rates"
- "Industry professional" → "10+ years, $10M+ in deals"

Cross-references: `./edit-lenses.md` (specificity lens), `./editing-principles.md` (specific over generic principle).

### 6. Avoid generic, over-used, and academic phrasing

Verbose, academic phrasing and purple prose are not desirable for online audiences. Replace formal connectors ("however," "moreover," "thus") with sentence-starts that flow conversationally. Replace academic constructions ("it is important to note that...") with direct statements.

Cross-reference: `../../_shared/references/ai-writing-patterns.md` for the catalog of phrases to remove.

### 7. Avoid giving posts titles

Remove any titles you're tempted to put in. Just write the post. The first line is the hook. If it works, the post doesn't need a title in the body.

(This applies to social posts and similar short-form content. For blog posts, articles, and longer pieces with publication context, titles are warranted — calibrate to medium.)

### 8. Remove and rewrite anything similar to disallowed phrases

The anti-AI catalog (`../../_shared/references/ai-writing-patterns.md`) lists specific items. The rule generalizes: any phrase that reads as AI-generated, AI-polished, or stylistically over-formal for online context gets the same treatment — remove or rewrite.

## Why these rules

Internet writing rewards different qualities than print writing. Where print rewards completeness and density, online rewards scannability and momentum. Where print readers commit to a piece before reading, online readers can leave at any sentence. The rules calibrate to that asymmetry.

## When to relax these rules

These rules apply to:
- Social posts (LinkedIn, X, Threads, Bluesky)
- Newsletter copy
- Blog posts and articles for general audiences
- Sales / marketing copy

These rules apply less or not at all to:
- Academic writing — formal connectors and dense paragraphs are expected
- Technical documentation — readability is structured differently (lists, tables, code blocks)
- Literary fiction — voice and rhythm dominate over scannability
- Long-form journalism in publications that calibrate to print conventions

`modes/humanize` defaults to applying these rules. If the user names a context where they don't apply (academic paper, technical doc, novel chapter), respect the context and adjust.

