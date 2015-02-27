{% extends 'display_priority.tpl' %}

{%- block header -%}
{%- if nb.metadata.post -%}
---
layout: post
title: "{{ nb.metadata.post.title }}"
cover: "{{ nb.metadata.post.cover }}"
coveralt: "{{ nb.metadata.post.coveralt }}"
tags:
{%- for tag in nb.metadata.post.tags %}
  - {{ tag }}
{%- endfor %}
---
{%- endif %}

{:.preamble}
This post is also available as an IPython notebook which may be
[downloaded]({{'{{'}} "/downloads/{{ resources.metadata.name }}.ipynb" | prepend: site.baseurl {{'}}'}})
or [viewed online]({{'{{'}} site.nbviewer_root {{'}}'}}/downloads/{{ resources.metadata.name }}.ipynb).
{% endblock header %}

{% block in_prompt %}
{% endblock in_prompt %}

{% block output_prompt %}
<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>
{% endblock output_prompt %}

{% block input %}
{{ '```python' }}
{{ cell.input }}
{{ '```' }}
{% endblock input %}

{% block pyerr %}
{{ super() }}
{% endblock pyerr %}

{% block traceback_line %}
{{ line | indent | strip_ansi }}
{% endblock traceback_line %}

{% block pyout %}

{% block data_priority scoped %}
{{ super() }}
{% endblock %}
{% endblock pyout %}

{% block stream %}
{{ output.text | indent }}
{% endblock stream %}

{% block data_svg %}
![svg]({{ output.svg_filename | path2support }})
{% endblock data_svg %}

{% block data_png %}
![png]({{ output.png_filename | path2support }})
{% endblock data_png %}

{% block data_jpg %}
![jpeg]({{ output.jpeg_filename | path2support }})
{% endblock data_jpg %}

{% block data_latex %}
{{ output.latex }}
{% endblock data_latex %}

{% block data_html scoped %}
{{ output.html }}
{% endblock data_html %}

{% block data_text scoped %}
{{ output.text | indent }}
{% endblock data_text %}

{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) }}
{% endblock markdowncell %}

{% block headingcell scoped %}
{{ '#' * cell.level }} {{ cell.source | replace('\n', ' ') }}
{% endblock headingcell %}

{% block unknowncell scoped %}
unknown type  {{ cell.type }}
{% endblock unknowncell %}
