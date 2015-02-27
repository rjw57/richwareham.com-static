---
layout: post
title: "Fonts from old ROMs with Python"
cover: "images/acorn-rom.png"
coveralt: ""
tags:
  - python
  - notebook
---

{:.preamble}
This post is also available as an IPython notebook which may be
[downloaded]({{ "/downloads/2015-02-03-font-from-bbc-rom.ipynb" | prepend: site.baseurl }})
or [viewed online]({{ site.nbviewer_root }}/downloads/2015-02-03-font-from-bbc-rom.ipynb).

# Introduction

For a personal project recently I needed a simple monospaced 8x8 pixel font. I
could, of course, make my own but I thought it'd be nice for nostalgia reasons
to try and extract the Acorn 8x8 font used in the old [BBC
Microcomputer](http://en.wikipedia.org/wiki/BBC_Micro). Using Python we can
directly extract the font from a zipfile containing a ROM image which we
download from the web. We can then use the [imgur](https://imgur.com) API to
upload the resulting font directly to the web.

# Implementation

You can find a copy of the [BBC Model B memory
map](http://www.8bs.com/mag/32/bbcmemmap2.txt) online. The relevant section for
our needs is:

```
PAGE 192 (&C0) to 194 (&C2) : OS ROM

C000-C2FF Character font lookup table
```

This tells us that the character font table is in the first 0x300 (or 768) bytes
of the OS ROM. The OS ROMs are available from multiple sources but there is a
[page](http://www.bbcmicrogames.com/roms.html) on a BBC Micro games site which
has a link.


```python
OS_ROM_URL = 'http://www.bbcmicrogames.com/roms/os12.zip'
```

This is a zip file and so we can use the Python ``zipfile`` module to examine
the file after downloading it into a ``bytes`` object via the ``requests``
library:


```python
import requests         # downloading the zipfile
from io import BytesIO  # treating a bytes object as file
import zipfile          # parsing the zipfile
```


```python
# Fetch the ROM and check that the GET succeeded
os_rom_zip_req = requests.get(OS_ROM_URL)
assert os_rom_zip_req.status_code == 200
```


```python
# Parse the body as a zip file
os_rom_zip = zipfile.ZipFile(BytesIO(os_rom_zip_req.content))
```

There should only be one file in the archive which is the one we want:


```python
print('Archive contents: ' + ','.join(os_rom_zip.namelist()))
assert len(os_rom_zip.filelist) == 1
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Archive contents: OS12.ROM


So, we want to get the first 0x300 bytes:


```python
font_table = os_rom_zip.read(os_rom_zip.filelist[0])[:0x300]
```

We can use the ``bitarray`` module along with ``numpy`` to extract the character
font as a 1-bit array. The characters are stored as one byte per row and so our
final font array should be 8 columns wide and 8 &times; number of characters
high.


```python
import numpy as np
from bitarray import bitarray
```


```python
font_table_array = bitarray(endian='big')
font_table_array.frombytes(font_table)
font = np.array(font_table_array.tolist()).reshape((-1, 8))

n_chars = font.shape[0] // 8
print('Number of characters: {0}'.format(n_chars))
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Number of characters: 96


Let's look at the first few characters just to check:


```python
%matplotlib inline
from matplotlib.pyplot import *

imshow(font[:8*3, :], interpolation='none', cmap='gray')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>




    <matplotlib.image.AxesImage at 0x7f344fc0db38>




![png]({{ "/images/2015-02-03-font-from-bbc-rom_files/2015-02-03-font-from-bbc-rom_17_1.png" | prepend: site.baseurl }})


It would be nice to see the entire font as one image. Let's first split it into
one array per character:


```python
char_arrays = np.split(font, n_chars)

# check that we've split correctly
imshow(char_arrays[20], interpolation='none', cmap='gray')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>




    <matplotlib.image.AxesImage at 0x7f344fbebd68>




![png]({{ "/images/2015-02-03-font-from-bbc-rom_files/2015-02-03-font-from-bbc-rom_19_1.png" | prepend: site.baseurl }})


Now we do some advanced juggling to reshape the character array:


```python
font_image = np.vstack(tuple(
    np.hstack(row).reshape((8, -1)) for row in np.array(char_arrays).reshape((-1, 16, 8, 8))
))

print('Generated font image of shape: ' + 'x'.join(str(x) for x in font_image.shape))

imshow(font_image, cmap='gray', interpolation='none')
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Generated font image of shape: 48x128





    <matplotlib.image.AxesImage at 0x7f344fb65208>




![png]({{ "/images/2015-02-03-font-from-bbc-rom_files/2015-02-03-font-from-bbc-rom_21_2.png" | prepend: site.baseurl }})


And we're a winner. The only thing left to do is to save it as an image for some
further processing. We'll use the ``imgurpython`` library to upload our result
directly to imgur. I've created a file called ``imgur-credentials.json``
containing the client id and secret I obtained by registering an application at
https://api.imgur.com/. The file looks something like this:

```json
{
    "clientId": "some magic hex string",
    "clientSecret": "another magic hex string"
}
```

The first thing to do is to create an imgur client to upload the file:


```python
import json
from imgurpython import ImgurClient

imgur_creds = json.load(open('imgur-credentials.json'))
imgur_client = ImgurClient(imgur_creds['clientId'], imgur_creds['clientSecret'])
```

Using the ``pillow`` library we can save the image to a temporary file and the
upload it. Note the use of the ``with`` statement to make sure that the
temporary file is deleted.


```python
import tempfile
from PIL import Image

with tempfile.NamedTemporaryFile(suffix='.png') as tf:
    Image.fromarray(np.where(font_image, 255, 0).astype(np.uint8)).save(tf.name)
    upload_result = imgur_client.upload_from_path(tf.name)
print('Image uploaded to: {0}'.format(upload_result['link']))
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>

    Image uploaded to: http://i.imgur.com/7mZVBee.png


IPython has some built-in support for displaying images from URLs. Let's use
that to look at the result:


```python
from IPython.display import Image
Image(upload_result['link'])
```

<div class="ipynb-output-prompt clearfix">
  <div class="pull-left"><i class="fa fa-arrow-down"></i></div>
  <div class="pull-right"><i class="fa fa-arrow-down"></i></div>
</div>




![png]({{ "/images/2015-02-03-font-from-bbc-rom_files/2015-02-03-font-from-bbc-rom_27_0.png" | prepend: site.baseurl }})



# Conclusion

This little post has shown how we can extract fonts directly from old
microcomputer ROM images with Python. As a bonus, we upload the resulting font
back to the web via the imgur API.


```python

```
