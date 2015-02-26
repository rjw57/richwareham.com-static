---
layout: page
title: Articles
permalink: /articles/
theme: blue
---

A list of all articles which are on my site can be found below. They are
ordered by year and month.

{% assign year = null %}
{% assign month = null %}
{% for post in site.posts %}
  {% capture postyear %}{{ post.date | date: "%Y" }}{% endcapture %}
  {% capture postmonth %}{{ post.date | date: "%B" }}{% endcapture %}

  {% if year != postyear %}
    {% assign year = postyear %}
    {% assign month = null %}
# {{ year }}
  {% endif %}

  {% if month != postmonth %}
    {% assign month = postmonth %}
## {{ month }}
  {% endif %}

  <a href="{{ post.url }}">{{ post.title }}</a>
{% endfor %}
