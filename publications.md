---
layout: page
title: Publications
permalink: /publications/
theme: indigo
icon: rw:publications
---

Here are my publications sorted by year. It includes both conference and
journal articles. The list itself is imported from the [CUED Publications
Database](http://publications.eng.cam.ac.uk/) which may be more up to date and
is more use if you want to search or filter by a particular topic or
publication type. There is also a machine-readable [JSON
version](publications.json) available.

{% jsonball pubs from file publications.json %}

{% assign year = "" %}
{% for pub in pubs %}
  {% capture pubyear %}{{ pub.timestamp | divided_by: 1000 | date: '%Y' }}{% endcapture %}

  {% if pubyear != year %}
# {{ pubyear }}
  {% endif %}

  {% assign year = pubyear %}

  <p><pub-reference>
    <pub-authors>
      {% for c in pub.creators %}
        {% if c.name.family and c.name.given %}
          <pub-author>{{c.name.family}}, {{c.name.given}}</pub-author>
        {% elsif c.name.family %}
          <pub-author>{{c.name.family}}</pub-author>
        {% endif %}
      {% endfor %}
    </pub-authors>
    {% if pub.timestamp %}
      <pub-date>{{ pub.timestamp | divided_by: 1000 | date: '%Y' }}</pub-date>
    {% endif %}
    {% if pub.title %}
      {% if pub.uri %}
        <pub-title><a href="{{pub.uri}}">{{ pub.title }}</a></pub-title>
      {% else %}
        <pub-title>{{ pub.title }}</pub-title>
      {% endif %}
    {% endif %}
    {% if pub.event_title %}
      <pub-event>{{ pub.event_title }}{% if pub.event_location %},
        {{ pub.event_location }}{% endif %}</pub-event>
    {% endif %}
    {% if pub.publication %}
      <pub-publication>{{ pub.publication }}
      {% if pub.volume %} ({{ pub.volume }}){% endif %}
      {% if pub.pagerange %} pp. {{ pub.pagerange }}{% endif %}</pub-publication>
    {% endif %}
    {% if pub.issn %}<pub-additional>ISSN {{ pub.issn }}</pub-additional>{% endif %}
  </pub-reference></p>
{% endfor %}
