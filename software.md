---
layout: page
title: Software
permalink: /software/
theme: purple
icon: rw:software
---

# Dual-Tree Complex Wavelet Transform Library

I created a Python implementation of the Dual-Tree Complex Wavelet Transform
library and some associated algorithms. Currently the library supports the
following features:

* 1D, 2D and 3D forward and inverse DT-ℂWT;
* Locally affine 2D image registration and warping (aka "optical flow") using a method outlined in [
  Efficient Registration of Nonrigid 3-D Bodies](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=5936113&tag=1);
* Keypoint detection and localisation;
* OpenCL acceleration of the forward  DT-ℂWT;
* [Fully tested](https://travis-ci.org/rjw57/dtcwt);
* [Open Source](https://github.com/rjw57/dtcwt) and BSD-licensed;
* Python 2 and 3 compatible.

## Documentation

[Further documentation](https://dtcwt.readthedocs.org/) for the library
including example scripts, API reference and more information is available.

## Installation

Source code can be found on [Github](https://github.com/rjw57/dtcwt) and
installation is via ``pip`` or ``easy_install``:

```console
$ pip install dtcwt
```

