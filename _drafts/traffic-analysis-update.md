---
layout: post
title: "Can we predict England's traffic?"
coveralt: "An image of out poster"
cover: images/srf-meeting-poster-sep-2014.jpg
---

In September 2014, we presented a poster on some of the ancillary research I am
doing as part of my latest project supported by the [Centre for Sustainable
Road Freight](http://sustainableroadfreight.org). A [PDF of the
poster]({{site.url}}/downloads/srf-meeting-poster-sep-2014.pdf) is available to download for
those that are interested. The [source for the
poster](https://git.csx.cam.ac.uk/x/eng-sigproc/u/rjw57/srf/docs/poster-sep-2014.git)
is hosted on the University git service.

# Overview

The poster focusses on a single part of our wider research project on gathering
traffic flow data. Part A of the project aims to infer traffic flow directly
from video streams but knowing the current state of the world is only one part
of the problem; we are also investigating what techniques can be used to
predict the near future.

# Data wrangling

In [a previous post]({% post_url 2013-06-19-realtime-traffic-data %}) I
outlined some of the basic steps required to get hold of the UK Highways
Agency's real time data feed and wrangling it in Python. I recommend reading
that post if you're interested in the details of how the data is fetched and
parsed.

## What data is available?

The UK Highways Agency publish an XML document four times an hour which gives
the latest measurements for stretches of roads (or *links*) in England. A link
has a direction; each carriageway of a road will appear as a separate link but
a link may have multiple lanes. This information includes the current traffic
flow (vehicles/hour), mean speed (km/hour) and occupancy (%). An occupancy of
100% means that the road is fully occupied, nose-to-tail, on each lane.

## How do you get it?

The XML document itself is available via a public URL which may simply be
fetched. We have developed an automated system based in the Cloud which fetches
this document every 15 minutes, parses the XML and strips the information we
currently do not use. The XML stream itself is 120MB an hour and so this "data
reduction" step is important. We have a full archive of the XML stream for
around six months which is nearly 150GB in size even when compressed.

## How do you store it?

Our system in the cloud does two things. Firstly it provides an archive of the
day's traffic flows, occupancies and speeds which is downloaded and integrated
into a local SQLite database on our site. This database is the source for the
time-series data for individual links. The cloud based system also translate
the current state of England's traffic into a JSON-formatted document which can
easily be consumed by our web-based visualisation tool (XML, despite its
web-heritage, is rather inconvenient as a file format for today's web.) On a
more technical note, our cloud service also supports CORS (Cross-Origin
Resource Sharing) which is again a technical requirement for making use of the
data in our visualisation platform.

# Analysis

... Use [NMF].

# Prediction

# Summary

# References

* [nmf]

[nmf]: http://example.com/ "Non-negative matrix factorisation."
