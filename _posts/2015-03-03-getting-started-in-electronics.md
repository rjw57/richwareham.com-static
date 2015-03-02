---
layout: post
title: Getting Started with Electronics
cover: images/pcb-board.jpg
---
# Introduction

Towards the end of 2014 I decided that I wanted to learn digital electronics.
As someone who would self-identify as a software person I only had a relatively
wooley understanding of what happened at the "sand layer" of my computer. I've
set myself the project of designing and making a 1980s-era computer called
"Búri". I've recorded a few YouTube videos on it:

<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PLQdwYJ5AuTolZuQIYEujwqP3wV1qRbEa8" frameborder="0" allowfullscreen></iframe>

This post covers the "bootstrapping" process I went through to get myself to a
place where I could start learning electronics. Its the set of things I wish I
knew when I started.

# The essentials

Unlike software, electronics is fundamentally concerned with individual
*things*. And the thing about *things* is that the incremental cost of making
and delivering an individual *thing* is far greater than software. (Making a
copy of a piece of software is very nearly free.) Hence you'll need to spend
some money. I spent quite a bit of money but if I were to bootstrap again, this
is what I'd buy:

* £5.48 - [Arduino UNO-alike](http://www.ebay.co.uk/itm/UNO-R3-ATmega328P-CH340T-USB-Arduino-Compatible-Microcontroller-Board-UK-STOCK-/181678624617).
* £3.73 - [Solderless breadboard, wires and power supply](http://www.ebay.co.uk/itm/MB-102-830-Point-Solderless-PCB-Breadboard-Jump-Cable-Wires-65pcs-Power-Supply-/360736049270).
* £16.74 - [Electronics component starter kit](http://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=272_276&products_id=2009).

Prices inclusive of postage and correct at time of writing. Total cost: £25.95
or, again as of writing, around \$45 (US). Note that I'm not endorsing these
individual eBay sellers; YMMV when ordering from China.  I was also lucky in
that my Dad, on hearing of my new hobby, found a large box of chips, resistors,
capacitors, etc. in the garage. Most of my projects have now been driven more
by what I have for free in those boxes rather than what I've bought.

You can never have enough solderless breadboards. I bought a A4-sized
whiteboard from Poundland and stuck breadboards to it. This is a lot cheaper
than buying one of the metal-backed "advanced" breadboard modules. You can see
it in action in the videos above and, in an earlier state, below:

<iframe width="560" height="315" src="https://www.youtube.com/embed/lmBjuM0IS_4" frameborder="0" allowfullscreen></iframe>

*(The video itself is the first test of using a
[MAX7219](http://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf) chip
to drive a set of seven segment displays from the Big Box. This ended up
forming the core of the debug board for my homebrew 6502 computer.)*

## Less essential essentials

Aside from discrete components like resistors, capacitors and LEDs, if you want
to play with digital electronics like I did you'll need some
[7400 series logic](http://en.wikipedia.org/wiki/List_of_7400_series_integrated_circuits).
I inherited a lot from my Dad in
the Big Box O' Joy. That being said, the chips you'll definitely want a handful
of are:

* 74HC00 - NAND gates.
* 74HC02 - NOR gates.
* 74HC04 - NOT gates.
* 74HC74 - D-type flip-flops.
* 74HC165 - 8-bit "output" shift register.
* 74HC595 - 8-bit "input" shift register.

The latter two chips are useful if you're using an Arduino to drive lots of
outputs or getting lots of inputs. You'll be surprised at how small "lots" can be.

There's a good
[Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA) video
on the use of flip-flops in computer memory if you don't know your "D-type"s
from your "JK-type"s.

# Knowledge

Once you've got your equipment, you need to start learning.  I started with a
little basic electronics knowledge from school and a couple of courses at
University.  I was rather dismissive of electronics ad University viewing it as
a subject deeply steeped in "magic". As I've gotten older, I've realised that
electronics people viewed software as similarly being the domain of wizards and
sorcery. Such is any skill when viewed from outside.

That being said I was aware, perhaps distantly, of the following:

*   Voltage and current are different like "pressure" and "flow" are different.
    Current is the flow of electrons and voltage is how much those electrons
    want to flow.
*   Capacitors let *alternating current* pass but block *direct current*.
*   Diodes let current flow in one direction only.
*   Transistors act like an electrically controlled switch although I was more
    than a little fuzzy on the difference between NPN, PNP, bipolar junction,
    MOSFET, etc, etc.
*   Resistors obey [Ohm's law](http://en.wikipedia.org/wiki/Ohm%27s_law).
    (Otherwise known as the **V**ery **I**mportant **R**ule.)
*   [Kirchhoff's circuit
    laws](http://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws). (Otherwise
    known as "current and voltage don't appear or disappear by magic".)

Of these, the first is the most important. If you're not sure of the difference
between voltage and current you're going to have a bad time and you should
watch some YouTube videos to get a good handle on the difference.

*Aside: more correctly, I was aware that current is the flow of the places
where electrons want to be. [Conventional
positive-to-negative](http://en.wikipedia.org/wiki/Electric_current#Current)
current flow predates the discovery that electrons are negatively charged!*

I had, therefore, something of a schoolboy electronics knowledge with some
pretty large gaps but YouTube provided some important gap-filling mortar. I
can't stress how useful being able to sit down with a cup of tea and watch the
odd ten minutes of electronics tutorial videos was.

## A first project

The first circuit that almost anyone does these days is the Arduino "blinking
LED" circuit. This consists of an LED, a resistor and an Arduino. There's not
much to that but I like to try and learn a little bit of theory from everything
I do. The first question which popped into my head was "why do we need the
resistor?" I'll let the interested reader Google for better explanations than I
could write here but suffice it to say that I found it pleasing to be able to
calculate what value that resistor should have. Even the simplest of circuits
can be a learning opportunity.

From deep in my old bedroom in my parents' house came the book
[Adventures with Microelectronics](http://www.amazon.co.uk/Adventures-Microelectronics-Tom-Duncan/dp/0719536715).
I'm sure many similar books exist which were printed *after* the colours brown
and yellow went out of fashion. This book has a few simple circuits which can
be built on a breadboard and which cover the basics of wiring things up,
designing oscillators, etc. If you could find an introductory e-book on
something Arduino related, that'd probably be just as good. Working through the
book was the work of a single day but was fun to "get my feet wet".

## A stretch project

I found it important to set a "stretch goal": a project which seemed imposing
and difficult to begin with but could be broken down into stages which would
spark off simple projects along the way. As outlined in the introuction, I
chose to implement a 1980s-style microcomputer. The thought was that if I can
get to the point where I can compile C, I had "closed the gap" in my knowledge
between chip and code.

# YouTube: let a thousand lectures bloom

YouTube is an amazing resource for learning while in the bath. Queue up some
videos, draw some suds and lie and relax. If you;re learning electronics,
searching for "arduino" will consume many happy hours. If you want some
specific recommendations:

*   [Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA).
*   [Julian Ilett](https://www.youtube.com/user/julius256). His "postbag"
    segment lets you in to all the fun little electronics modules you can get
    from eBay.
*   [EEVblog "Fundamentals Friday"](https://www.youtube.com/playlist?list=PLvOlSehNtuHtWlH0UOZNtOn-FlFCn1GYw)
    YouTube playlist.
*   [The Ben Heck Show](https://www.youtube.com/user/thebenheckshow). This is
    more for inspiration than eductaion but is still fun.

# Conclusions

This post contains some of what I wished I knew when starting out in
electronics. Specifically, it gives an initial, affordable, shopping list. I
hope you find it useful!

