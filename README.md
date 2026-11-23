[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/wat-yuichi/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/wat-yuichi/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD ON MONDAY — 23 November 2026

One picture that sums up the world news of **Monday, 23 November 2026**,
drawn as the front page of a one-page newspaper: a dated masthead, six
story cards with hand-drawn pictograms, and a ticker of four shorter
items from the same day.

## The six stories

1. **Ukraine** — Russia's overnight barrage of 153 drones hit railway
   stations, a locomotive depot and power substations across 12 regions
   and Kyiv; 6 killed and 32 injured since the evening. Zelenskyy said
   intelligence points to further strikes being prepared, while the
   Kremlin floated new trilateral talks.
2. **Khartoum, Sudan** — the UN and the US condemned drone strikes on
   homes and a UN building in the capital; at least 4 people were
   killed, including a 10-year-old. The army alleges the drones were
   launched from Ethiopia — an unverified claim.
3. **Seoul, South Korea** — President Lee Jae Myung's Monday reshuffle
   nominated former justice minister Kang Kum-sil to lead the National
   Intelligence Service, the first woman picked for the post since the
   agency was founded in 1961, alongside new foreign and unification
   ministers.
4. **Yerevan, Armenia** — Prime Minister Pashinyan published a draft
   constitution that drops the reference to reunification with
   Karabakh, removing Azerbaijan's key objection to a formal peace
   treaty; he vowed to resign if a referendum rejects it.
5. **Virginia & Oregon, USA** — the two states became the first to sue
   Elon Musk's SpaceX / X over Grok's "spicy mode" generating
   sexualised images, including of children, under state
   consumer-protection laws.
6. **Bridgetown, Barbados** — closing the Bridgetown Special Summit on
   AI Safety, UN Secretary-General Guterres called for talks on a
   multilateral AI risk-management framework within a year, warning AI
   is driving "the biggest transfer of power in the history of
   humankind" from states to a few companies.

Ticker: Zelenskyy confirms Ukraine's seven sea drones sank the Russian
corvette Merkury in Benghazi and the UN urges a probe • Trump says he
is inclined to resume strikes on Iran after the New Year if there is no
deal • Don Toliver postpones his London O2 show to 15 December after an
"unknown substance" forced the evacuation of Manchester's Co-op Live •
WHO says fighting in Ituri, DR Congo, is disrupting the Ebola response.

See [NEWS.md](NEWS.md) for the source behind every item.

## How it is made

`tools/generate_image.py` draws the whole page with Pillow — masthead,
cards, pictograms and ticker — using the Noto fonts, then checks the
result against the bounty limits (≤ 1024×1024 px, ≤ 1 MiB) before
finishing. `main.ts` copies the finished `entry.png` into the output
directory named by `MAKEFUN_OUTPUT_DIR` (default `./output`).

## Layout

- `entry.png` — the delivered picture (1024×1024)
- `main.ts` — entry point; copies `entry.png` to the output directory
- `tools/generate_image.py` — the drawing program that produces `entry.png`
- `NEWS.md` — sources and reporting notes for each story
- `LICENSE` — MIT
