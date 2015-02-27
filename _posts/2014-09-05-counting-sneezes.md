---
layout: post
title: "Counting Sneezes from the Web"
cover: "images/sneeze.jpg"
coveralt: "CC BY-NC-ND foshydog@flickr"
tags:
  - python
  - notebook
---

{:.preamble}
This post is also available as an IPython notebook which may be
[downloaded]({{ "/downloads/2014-09-05-counting-sneezes.ipynb" | prepend: site.baseurl }})
or [viewed online]({{ site.nbviewer_root }}/downloads/2014-09-05-counting-sneezes.ipynb).

The [sneeze count](http://sneezecount.joyfeed.com/) website catalogues one
person's sneezes since 2007. A work colleague asked how difficult it would be to
extract a list of timestamps from the site. Could we then plot sneezes over
time? This post shows how easy this is to do using Python.

# Fetching the data

Conveniently there is an RSS feed available for the site which can be fetched
via Python's built in [urlopen](https://docs.python.org/3/library/urllib.request
.html#urllib.request.urlopen) function:


```python
from urllib.request import urlopen
print('...')
print('\n'.join(urlopen('http://sneezecount.joyfeed.com/feed').read().decode('utf8').splitlines()[20:30]))
print('...')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    ...
    	<item>
    		<title>Four thousand and nineteen</title>
    		<link>http://sneezecount.joyfeed.com/four-thousand-and-nineteen/</link>
    		<comments>http://sneezecount.joyfeed.com/four-thousand-and-nineteen/#comments</comments>
    		<pubDate>Fri, 22 Aug 2014 12:41:25 +0000</pubDate>
    		<dc:creator><![CDATA[Peter]]></dc:creator>
    				<category><![CDATA[Sneezes]]></category>
    
    		<guid isPermaLink="false">http://sneezecount.joyfeed.com/?p=8608</guid>
    		<description><![CDATA[Seesaw, Twycross Zoo Moderate to strong &#8220;I&#8217;m not heavy enough. And you&#8217;re too heavy.&#8221;]]></description>
    ...


There is also a ``paged`` query parameter whch lets one get the next page of
results:


```python
from urllib.request import urlopen
print('...')
print('\n'.join(urlopen('http://sneezecount.joyfeed.com/feed?paged=2').read().decode('utf8').splitlines()[20:30]))
print('...')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    ...
    	<item>
    		<title>Four thousand and nine</title>
    		<link>http://sneezecount.joyfeed.com/four-thousand-and-nine/</link>
    		<comments>http://sneezecount.joyfeed.com/four-thousand-and-nine/#comments</comments>
    		<pubDate>Sat, 09 Aug 2014 17:09:39 +0000</pubDate>
    		<dc:creator><![CDATA[Peter]]></dc:creator>
    				<category><![CDATA[Sneezes]]></category>
    
    		<guid isPermaLink="false">http://sneezecount.joyfeed.com/?p=8587</guid>
    		<description><![CDATA[Dining room, Malt Barn, Brize Norton Moderate Accepting the offer of an elderflower Prosecco]]></description>
    ...


Python also has a built in XML parsing module, the
[ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
module. Usage is, *ahem*, elementary:


```python
import xml.etree.ElementTree as ET

def parse_xml_url(url):
    tree = ET.parse(urlopen(url))
    return tree.getroot()

root = parse_xml_url('http://sneezecount.joyfeed.com/feed?paged=2')
print(root)
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    <Element 'rss' at 0x7f958d5ccf70>


An RSS feed encodes each post with an ``item`` tag and each publication date
within the item as a ``pubDate``. A quick and dirty hack to extract all dates
from an RSS feed is simply to list all the ``pubDate`` elements. According to
[WordPress's documentation](http://codex.wordpress.org/WordPress_Feeds#RSS_feed_
time_and_date_format), the ``pubDate`` tages are RFC822 dates. Python has a
module to deal with that too! The
[email.utils](https://docs.python.org/2/library/email.util.html) module has a
``parsedate`` function. The value can be passed directly to ``time.mktime()`` to
get a timestamp.


```python
from email.utils import parsedate
import time

def extract_dates(root):
    return list(time.mktime(parsedate(elem.text)) for elem in root.iter('pubDate'))

print(', '.join(str(t) for t in extract_dates(root)))
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    1407600579.0, 1407520308.0, 1407389858.0, 1407381140.0, 1407344647.0, 1407255800.0, 1407141500.0, 1407069426.0, 1407009164.0, 1406970003.0


To get dates for a given feed, therefore, we need simply page through the feed
starting at page 1 until we get a result with no items.


```python
from urllib.parse import urljoin
from urllib.request import HTTPError

def dates_from_feed_url(url):
    paged = 0
    all_dates = []
    while True:
        paged += 1
        page_url = urljoin(url, '?paged={0}'.format(paged))
        try:
            dates = extract_dates(parse_xml_url(page_url))
        except HTTPError:
            # Interpret a HTTP error (e.g. 404) as us reaching the end of the list
            break
        all_dates.extend(dates)
        if len(dates) == 0:
            break
    return all_dates

# Test with a feed URL for a single month:
ts = dates_from_feed_url('http://sneezecount.joyfeed.com/2014/08/feed')
print(', '.join(str(t) for t in ts))
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    1408707685.0, 1408628545.0, 1408563641.0, 1408537639.0, 1408439866.0, 1408275986.0, 1408256591.0, 1408167669.0, 1408131465.0, 1407820127.0, 1407600579.0, 1407520308.0, 1407389858.0, 1407381140.0, 1407344647.0, 1407255800.0, 1407141500.0, 1407069426.0, 1407009164.0, 1406970003.0, 1406870597.0


We can get all dates for all time by using the full feed URL:


```python
timestamps = dates_from_feed_url('http://sneezecount.joyfeed.com/feed')
```

If we look at the first page of the website, as of writing there are four
thousand and nineteen sneezes. Let's just ckeck that we've got them all:


```python
print('Fetched {0} sneeze timestamps'.format(len(timestamps)))
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Fetched 4019 sneeze timestamps


# Plotting

Let's use matplotlib to plot the timestamps. We first use some IPython magic to
load the pylab environment:


```python
%pylab inline
rcParams['figure.figsize'] = (14,9) # Set the default figure size
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Populating the interactive namespace from numpy and matplotlib



```python
plot(timestamps, np.arange(len(timestamps)))

title('Sneezes over time')
xlabel('Timestamp')
ylabel('Sneezes')

grid('on')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>


![png]({{ "/images/2014-09-05-counting-sneezes_files/2014-09-05-counting-sneezes_16_0.png" | prepend: site.baseurl }})


Possibly more interesting is a histogram of intervals between sneezes:


```python
# Use three hour bins out to 5 days
hist(np.diff(np.asarray(timestamps) / (60*60)), bins=np.arange(0, 5*24, 3))
title('Histogram of times between sneezes')
xlabel('Hours')
ylabel('Count')
grid('on')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>


![png]({{ "/images/2014-09-05-counting-sneezes_files/2014-09-05-counting-sneezes_18_0.png" | prepend: site.baseurl }})


# Summary

In this post we showed how the Python standard library has all the tools we
require to scrape a website and plot some interesting figures using data from
it.
