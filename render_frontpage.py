#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026 and save entry.png.

A one-page newspaper summary of the day's world news, drawn with Pillow
from fixed text and shapes only: no network, no clock, no randomness, so
two runs produce byte-identical output.

Stories were checked against reports published on 26 November 2026
(BBC, Reuters, The Guardian, NYT digests). Where outlets disagreed on a
figure it is left out rather than guessed: the Colombia siege is reported
without a hostage count, because counts in the day's coverage ranged
from about 20 to 76.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 243, 233)
INK = (24, 22, 18)
RED = (178, 34, 28)
NAVY = (18, 48, 88)
GREY = (104, 98, 88)
LIGHT = (255, 255, 255)
BLUE_TINT = (226, 236, 245)
WARM_TINT = (243, 231, 214)
RULE = (24, 22, 18)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}.ttf", size)


SERIF_B = lambda s: font("LiberationSerif-Bold", s)
SERIF = lambda s: font("LiberationSerif-Regular", s)
SANS_B = lambda s: font("LiberationSans-Bold", s)
SANS = lambda s: font("LiberationSans-Regular", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=1.28):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, label, color=RED):
    f = SANS_B(17)
    draw.text((x, y), label.upper(), font=f, fill=color)
    return y + 24


def headline(draw, x, y, width, text, size, fill=INK):
    f = SERIF_B(size)
    lines = wrap(draw, text, f, width)
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += int(size * 1.08)
    return y


def rule(draw, x0, y, x1, weight=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=weight)


def chip(draw, x, y, text):
    """Small filled tag, e.g. a dateline or section label."""
    f = SANS_B(15)
    w = int(draw.textlength(text, font=f)) + 18
    draw.rounded_rectangle([x, y, x + w, y + 24], radius=4, fill=NAVY)
    draw.text((x + 9, y + 4), text, font=f, fill=LIGHT)
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    right = W - mx

    # --- frame ---------------------------------------------------------
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # --- masthead ------------------------------------------------------
    d.text((mx, 26), "THE WORLD TODAY", font=SERIF_B(66), fill=INK)
    d.text((mx, 100), "THURSDAY 26 NOVEMBER 2026  ·  ONE PAGE, THE DAY'S NEWS",
           font=SANS_B(17), fill=GREY)
    rule(d, mx, 132, right, 4)
    rule(d, mx, 139, right, 1)

    # --- lead story: Nvidia -------------------------------------------
    y = 156
    chip(d, mx, y, "LEAD  ·  TECHNOLOGY")
    y = kicker(d, mx + 268, y + 1, "Washington  ·  Silicon Valley", color=NAVY)
    y = headline(d, mx, y + 6, right - mx,
                 "Trump's rescue brings Huang back to Nvidia — and rattles the markets",
                 40)
    y = para(d, mx, y + 8, right - mx,
             "Donald Trump says he convinced Nvidia's board to reinstate Jensen Huang "
             "as chief executive, days after the chipmaker's boss resigned. S&P put "
             "Nvidia's AA credit rating on negative watch over governance concerns, "
             "and shares slid as politicians questioned the president's role.",
             SERIF(22), leading=1.3)
    rule(d, mx, y + 16, right, 2)
    y += 30

    # --- second row: two stories side by side --------------------------
    col_w = (right - mx - 28) // 2
    x2 = mx + col_w + 28
    top2 = y

    # Russia
    d.rounded_rectangle([mx, top2, mx + col_w, top2 + 178], radius=6, fill=BLUE_TINT)
    yy = kicker(d, mx + 16, top2 + 12, "War in Ukraine")
    yy = headline(d, mx + 16, yy + 2, col_w - 32,
                  "Russia's own figures show nearly 500,000 dead", 27)
    para(d, mx + 16, yy + 6, col_w - 32,
         "Moscow's data puts its war dead near half a million — as Russia passes "
         "its biggest military budget since Soviet times.",
         SANS(18), leading=1.3)

    # Cairo
    d.rounded_rectangle([x2, top2, x2 + col_w, top2 + 178], radius=6, fill=WARM_TINT)
    yy = kicker(d, x2 + 16, top2 + 12, "Egypt")
    yy = headline(d, x2 + 16, yy + 2, col_w - 32,
                  "31 killed as fuel tanker fire engulfs Cairo highway", 27)
    para(d, x2 + 16, yy + 6, col_w - 32,
         "A tanker crash on the capital's ring road set off a huge blaze; "
         "at least 25 more people were injured.",
         SANS(18), leading=1.3)

    y = top2 + 178 + 22
    rule(d, mx, y, right, 2)
    y += 22

    # --- third row: two stories side by side ---------------------------
    top3 = y
    yy = kicker(d, mx, top3, "Colombia")
    yy = headline(d, mx, yy + 2, col_w - 32,
                  "Hostages freed after 17-hour supermarket siege", 26)
    para(d, mx, yy + 6, col_w - 32,
         "Police stormed a supermarket in Cartagena and freed dozens of shoppers "
         "and staff; one gunman was killed.",
         SANS(18), leading=1.3)

    yy = kicker(d, x2, top3, "Trade")
    yy = headline(d, x2, yy + 2, col_w - 32,
                  "US unveils new tariffs on China, the EU and more", 26)
    para(d, x2, yy + 6, col_w - 32,
         "Washington plans fresh duties on China, the EU, Japan, South Korea and "
         "a dozen other economies; stocks fell on the news.",
         SANS(18), leading=1.3)

    y = top3 + 168
    rule(d, mx, y, right, 2)
    y += 20

    # --- also today strip ----------------------------------------------
    d.text((mx, y), "ALSO TODAY", font=SANS_B(17), fill=RED)
    y += 30
    thirds = (right - mx - 56) // 3
    items = [
        ("THANKSGIVING",
         "A powerful storm threatens the 100th Macy's Thanksgiving Day Parade "
         "in New York, with high winds and flooding on the East Coast."),
        ("SPACE",
         "Europe's Hera probe reveals close-up images of the asteroid hit in "
         "the test to defend Earth — a stadium-sized crater."),
        ("ASIA",
         "Pakistan's first astronaut is set to fly to China's Tiangong space "
         "station aboard the Shenzhou-24 mission."),
    ]
    for i, (label, text) in enumerate(items):
        x = mx + i * (thirds + 28)
        if i:
            d.line([(x - 14, y), (x - 14, y + 108)], fill=GREY, width=1)
        d.text((x, y), label, font=SANS_B(16), fill=NAVY)
        para(d, x, y + 26, thirds, text, SANS(17), leading=1.28)
    y += 122

    # --- footer ----------------------------------------------------------
    rule(d, mx, y, right, 1)
    d.text((mx, y + 12),
           "Sources: BBC, Reuters, The Guardian, NYT — Thursday 26 November 2026",
           font=SANS(15), fill=GREY)
    d.text((mx, y + 34),
           "make.fun news-image-20261126  ·  drawn summary, no photographs",
           font=SANS(15), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
