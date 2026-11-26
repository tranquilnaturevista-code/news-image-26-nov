# The World in One Day — Thursday 26 November 2026

[![News Image](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/tranquilnaturevista-code/news-image-26-nov/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/tranquilnaturevista-code/news-image-26-nov/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for the [make.fun bounty "Sum up 26 November's world news in one
image"](https://make.fun/bounty/news-image-20261126): a one-page newspaper
front page for **Thursday 26 November 2026**, drawn programmatically with
Pillow. The lead story is the Nvidia leadership drama — Trump says he
convinced the board to bring Jensen Huang back as CEO, S&P put the
company's AA rating on negative watch, and shares slid — and the page
carries five more stories: Russia's war dead near half a million by its
own figures, the deadly Cairo tanker fire, the freed hostages in
Cartagena, new US tariffs, and a storm threatening the 100th Macy's
Thanksgiving Day Parade, plus space and Asia notes along the bottom.

## How it works

- `render_frontpage.py` draws the page (1024×1024 PNG) from the story
  list below and saves it as `entry.png`. It uses no network, no
  randomness, and no timestamps: two runs produce byte-identical output.
- `main.py` is the entry program. It checks that `entry.png` is a whole
  PNG within the competition limits (at most 1024×1024 pixels, at most
  1 MiB) and copies it byte for byte to `/output/entry.png`, so the page
  the judge sees is exactly the page laid out here. It needs only the
  Python standard library.

## Stories in the image

- **Huang is back at Nvidia (lead).** Trump says he convinced Nvidia's
  board to reinstate Jensen Huang as chief executive; S&P put Nvidia's
  AA rating on negative CreditWatch over governance concerns, and shares
  slid as politicians questioned the president's role. (BBC, Reuters,
  26 November 2026)
- **Russia's own figures show nearly 500,000 dead in Ukraine.** Moscow's
  data puts its war dead near half a million, as Russia passes its
  biggest military budget since Soviet times. (BBC, 26 November 2026)
- **31 killed as a fuel tanker fire engulfs a Cairo highway.** A tanker
  crash on the capital's ring road set off a huge blaze; at least 25
  more people were injured. (BBC, 26 November 2026)
- **Hostages freed after a 17-hour supermarket siege.** Police stormed a
  supermarket in Cartagena, Colombia, and freed dozens of shoppers and
  staff; one gunman was killed. (BBC, The Guardian, 26 November 2026)
- **US unveils new tariffs on China, the EU and more.** Washington plans
  fresh duties on China, the EU, Japan, South Korea and a dozen other
  economies; stocks fell on the news. (NYT, 26 November 2026)
- **Also today:** a powerful storm threatens the 100th Macy's
  Thanksgiving Day Parade in New York; Europe's Hera probe reveals
  close-up images of the asteroid hit in the planetary-defence test — a
  stadium-sized crater; Pakistan's first astronaut is set to fly to
  China's Tiangong space station aboard Shenzhou-24. (BBC, Reuters,
  26 November 2026)

Where the day's outlets disagreed on a figure it is left out rather than
guessed: the Colombia item gives no hostage count, because counts in
coverage ranged from about 20 to 76. All stories are events that
happened, or were first reported, on 26 November 2026.

## Reproduce

```sh
python3 render_frontpage.py   # writes entry.png (deterministic)
python3 main.py               # writes /output/entry.png
```

Python 3.13 and Pillow are all that is needed to render; `main.py`
itself needs only the standard library.
