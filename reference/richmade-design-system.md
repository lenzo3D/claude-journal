# Richmade design system (for Richmade-branded material)

Use this for material that carries Richmade's own branding: non-legal documents, PDFs, proposals, reports and slide decks. It does **not** apply to client websites or client content, which follow each client's own brief.

Copied 28 Sep 2026 from the Richmade site repo (`~/Documents/AI Agency/site`): values from `css/styles.css` (the source of truth for values), and decisions from `DESIGN_BRIEF.md` sections 2, 3 and 8. `reference/sources.json` records the exact commits, and `scripts/check-sources.py` reports when the site has changed since. If Jake's latest instruction disagrees with this file, his instruction wins. Update this file to match.

## Colour

| Token | Hex | Use |
|---|---|---|
| Canvas | `#FFFFFF` | Page and slide background |
| Ink | `#0B0C0E` | Headings and body text |
| Ink secondary | `#55575D` | Captions, labels, metadata |
| Accent | `#0E63F4` | The one accent. Key numbers, links, underlines, a single highlight per page or slide |
| Accent hover | `#0A4FC7` | Pressed or hover state in interactive material only |
| Panel | `#F6F6F7` | Callout boxes, table header rows, sidebars |
| Line | `#E7E7E9` | 1px borders and table rules |
| Dark | `#0A0A0B` | Dark band (see below) |
| Dark secondary | `#A1A1A8` | Secondary text on the dark band |

The accent is never a background fill for a whole section, never a gradient, and never more than one hue. On the site, the dark band is used only for the closing call to action and the footer. The equivalent in a deck is the closing slide, and in a document the back cover. That mapping is an interpretation, not a stated decision, so confirm it with Jake the first time it matters.

## Type

- **Headings:** Schibsted Grotesk, weight 600 to 800 (700 by default), tracking about -0.025em, tight line height (about 1.04).
- **Body and UI:** Instrument Sans, weight 400 to 600.
- **Fallback:** "Helvetica Neue", Arial, sans-serif.
- Font files are in `reference/fonts/` (latin subset, woff2, SIL Open Font License). For desktop tools that need TTF or OTF, download the same families from Google Fonts.
- No other typefaces, ever. Never Inter, Space Grotesk or system-ui as brand type.

On the web: body 17px, heading scale ratio 1.25 (mobile) or 1.333 (desktop), lines no longer than 68 characters. For print and slides, keep the same ratios and the same line-length limit rather than the pixel sizes.

## Layout

- Left-align everything. Centre only a single closing statement.
- Whitespace is the luxury signal. When unsure, add space, not elements.
- Corner radius 14px for cards and panels, 8px for small elements. Don't round everything the same.
- On the web: max content width 1120px, 12 columns, 24px gutters, section padding 96px desktop and 64px mobile.

## Voice (applies to every word on Richmade material)

- Confident and plain, written to a busy business owner whose English may not be advanced. Short, concrete sentences with specific numbers. Lead with an outcome and a number.
- No em dashes. Use full stops, commas or colons.
- No chains of clipped fragment pairs ("Two people. No account managers."). At most one per document.
- Never promise a hard date Richmade can't hit, and never claim scarcity or credentials that aren't true (Richmade is not a PSG pre-approved vendor).
- Banned words: elevate, empower, unleash, seamless, cutting-edge, solutions, digital presence, passionate, innovative, world-class.

## Kill list (reject on sight)

Inter or system-ui as brand type, purple-blue gradients, emoji as icons, three identical centred cards, glassmorphism, stock photos (laptops, handshakes), the same radius on everything, testimonials without a real name and firm, lorem ipsum, centred body text, and any banned word.
