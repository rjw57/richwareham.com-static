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

Our central assumption is that all links exhibit similar patterns over the
course of a day. This matches our intuition that we expect morning, evening,
daytime and night time behaviours to be different for any given link but all
links will have some degree of, for example, "morning rush hour".

Traditionally this data reduction step would be performed by taking a large
number of "training" samples of daily traffic behaviour and using some
projection-based technique such as [Principal Component Analysis][pca] to
extract a small set of "basis vectors" or "components" which can be scaled and
summed together to approximate any of the training samples with minimal error.

These techniques are well known and often very useful as initial data reduction
step. The problem is that the basis vectors produced are not guaranteed to be
positive. Usually this is not a problem but in traffic analysis one of the few
things we can say with certainty is that speeds, occupancies and traffic flows
are positive.

Taking a naïve PCA of 40,000 traffic flow daily samples results in these
components:

![]({{site.url}}/images/pca-traffic-flow.svg)

The only directly interpretable component is the first cone which corresponds
to the normalised mean of all traffic flows. The rest are not very
illuminating. In the case of traffic analysis one has a lot of prior knowledge
available which does not obviously map onto these components.

Instead of PCA, we can make use of a relatively novel technique: [non-negative
matrix factorisation][nmf]. In this technique one forces all of the components
to be positive. The downside is that the factorisation is no-longer unique. To
combat this, one usually factorises while minimising some "sparseness measure".
In our case we factorise while trying to keep the components as "peak-like" as
possible. Fortunately the NMF implementation we are using, [scikit-learn][skl],
directly supports this. The non-negative fundamental components look like this:

![]({{site.url}}/images/nmf-traffic-flow.svg)

It is now far easier to directly interpret these components in terms of
"morning rush hour", "night time flow", etc.

By resolving our training flows onto these components we end up with 5
components which describe the flow on one link over an entire day rather than
one number for each quarter hour sample. This is around a 5% data reduction.

We may now reason using these components to derive "typical" component values
for each flow for each weekday. Typical results from this projection are shown
in the poster.

# Prediction

Data reduction is all well and good but it is all for naught if the reduced
data doesn't represent the actual data. To this end we investigated how well
our "typical week" will predict a new week which wasn't present in our training
data. To add some challenge, the new week included a Bank Holiday Monday which
wasn't present in the training set.

Reconstructing our "typical week" for each link resulted in surprisingly good
performance. Remember that this is the simplest form of prediction; we assume
that each week is like the typical week. Even with such a simple model our
prediction has a median relative error of only 7%. Plotting a scatter chart of
predicted flow versus actual flow showed a tight adherence to the perfect 1:1
correspondence line. The bank holiday was clearly visible in the predicted
output.

# Summary

We investigated whether non-negative matrix factorisation of traffic flows in
England could provide large scale data reduction with low error while providing
basis components which retained interpretable. We showed that even reducing
data to 0.25% of the original we could predict future flows with a median
relative error of 7%.

Given these results we intend to proceed with traffic prediction working
directly on the reduced traffic data which we believe to be a more tractable
problem than dealing with the full dataset directly.

# References

* [Non-negative Matrix Factorization (Wikipedia references)][nmf]
* [Principal Component Analysis][pca]
* [Scikit-learn][skl]: a Python package for machine learning

[nmf]: https://en.wikipedia.org/wiki/Non-negative_matrix_factorization#Others
[pca]: https://en.wikipedia.org/wiki/Principal_component_analysis
[skl]: http://scikit-learn.org/
