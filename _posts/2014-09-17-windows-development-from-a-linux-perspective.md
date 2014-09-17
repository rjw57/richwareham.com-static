---
title: Windows Development from a Linux Programmer's Perspective
cover: images/windows-8.1.jpg
coveralt: CC-BY vernieman@flickr
---

I recently had to do a little bit of Windows development after having managed
to avoid it for around seven years. This post documents my experiences from the
point of view of an experienced software developer from a non-Windows
background.

The precise reasoning behind why I needed to do some Windows development isn't
that important for this post but, for the curious, I've included a brief
summary at the end of the post. The short-version: I wanted to write a server
which would advertise itself over
[Zeroconf](https://en.wikipedia.org/wiki/Zero-configuration_networking) and
stream depth frames from a [Kinect for Windows
2](http://www.microsoft.com/en-us/kinectforwindows/) sensor over the network
using [ØMQ](https://en.wikipedia.org/wiki/%C3%98MQ).

# Don't fight the inevitable

It's a mistake to try and fight the common culture on a particular platform.
My usual tool for writing research software is Python. It is an excellent
language and ecosystem for writing scientific research software on Linux-like
platforms but there is quite the impedance mismatch on Windows. I decided that
it would be best to try and embrace the Windows development culture and write a
Kinect 2 streaming server "the Windows way".  This also meant I would avoid the
future problem of getting Python to talk to the Kinect for Windows SDK.

The "Windows way" in this case is undoubtedly .NET and Visual Studio. What
follows are some of my experiences trying to determine what the Windows way is
and following it. I should note that the last time I did any Windows
programming was a long time ago in a different job and in a completely
different field. It was also in C++. I've very little experience with .NET
development. This was the project to learn. [The
code](https://github.com/rjw57/streamkinect2.net) is available. Idiom-fixing
pull requests are very welcome.

# Visual Studio Express Edition

It's madness to charge people for the privilege of adding value to your
software platform so it's nice to see that Microsoft make the [express
edition](http://www.visualstudio.com/en-us/products/visual-studio-express-vs.aspx)
of Visual Studio available at zero-cost. It is, however, extremely confusing
that you need to know that you need the "for Windows Desktop" version in order
to actually develop programs; the similarly named "for Windows" edition being
good only for writing software for both users of Windows Phone OS.

(Aside: perhaps Apple might want to consider quite how many times people need
to pay a $99 bounty to write code for their OS, get their development tools,
get something onto one of their phones, etc. Development on Apple used to be a
dream in 2004. Ten years later it is a nightmare.)

Visual Studio itself is... OK. I don't really like tools which hide things from
you, particularly if you're a software developer. Visual Studio skirts the
boundary of "too much magic" but in general I didn't find myself worrying where
on disk a particular magic bit of configuration is stored.

I'm not really an IDE guy but I will admit that for an almost complete novice
.NET developer, the code-completion is useful. The quality of the MSDN
documentation, however, is pretty poor. One line summaries of methods, in
particular, are inexcusable. Also the MSDN website is really... slow... to...
browse. I'd rather have usage examples and discussion of APIs next to or within
the reference. Having them scattered all over MSDN makes quickly learning about
something pretty hard.

The [MSBuild](http://msdn.microsoft.com/en-us/library/0k6kkbsd.aspx) tool is a
welcome change since the last time I touched Windows development. Being able to
run tests, build code and even package up the results from the command line or
automated scripts is an absolute essential.

# C# and .NET

I'd say that C# is a very well designed language in that it is utterly
unsurprising. Designing something new to be unsurprising is very difficult and
it is a complement to C# to describe it as such. If you can get by in Object
Pascal and Java then you'll make yourself understood in C#. I suspect I was
programming with a thick C++ accent but I don't think I was being *too*
offensive to the C# idiom.

I like the Go-style divorce between namespaces/modules and file names on disk;
source code files are best organised for the convenience of the developer of a
library whereas namespaces are best organised for the convenience of a
consumer. Having this distinction recognised is welcome.

# External dependencies

This has traditionally where Windows has been the most painful. Thankfully I
only had three external dependencies.

* The [NetMQ](https://github.com/zeromq/netmq) .NET port of ØMQ is available
through the [NuGet](https://www.nuget.org/) package manager. NuGet is a
solution which should've existed ages ago. It's sad that it required a
third-party Open Source project to plug such a gaping hole.

* Apple's Bonjour API is exposed via COM objects. This necessitates the
installation of a MSI package to get all of Bonjour up and working but an
advantage of COM is that one doesn't need to hard-code or discover DLL paths in
your build system.

* The Kinect SDK itself is a bit of a pain. At the moment I don't actually have
access to a Windows 8 box and so I had to do some tricks to pull the DLLs out
from the installer package directly since it flat-out refuses to install on any
other version. (I with there was an option in MSI packages to only install a
subset of the contents.) This is only necessary on my current development
machine while I wait for a Windows 8 machine to become available. The Kinect
.NET API lives in the global assembly cache (GAC) and so, again, I don't need
to worry about hard-coding paths to find DLLs.

The handling of dependencies was actually the part of this whole project where
I was the most pleasantly surprised. NuGet has solved a lot of the problems
which I used to have with Windows development.

# Source control

Microsoft finally woke up to the fact that git is the source control system
which the cool kids are using. And no one more obviously yearns to be one of
the cool kids than Microsoft does at the moment. Visual Studio's git
integration is basic but functional. I didn't try to see how easy it was to
clone/push/pull/merge/etc from the GUI because I only used the GUI for simple
"commit all the changes" type activity. For everything else, I just used [git
for windows](http://git-scm.com/download/win) and Git bash. There's not much to
say about git bash: it's git and bash. Thankfully vim is included as well. I
ended up using vim to edit things like READMEs. Visual Studio's editor is
overkill for editing text files and I just couldn't get on with things like
[Notepad++](http://notepad-plus-plus.org/). I'm also not fashionable enough to
use Sublime Text. I suspect editors are just too personal a thing to change at
the drop of a hat.

While we're talking about git bash, the terminal ("console" in Micro-speak) is
appalling. It's 2014 and you should be able to a) resize the window and b) copy
and paste without resorting to hidden menus. Even [Windows
PowerShell](https://en.wikipedia.org/wiki/Windows_PowerShell) seems to have
been hit with the same ugly stick.

# Testing

The unit test framework in Visual Studio is perfectly acceptable. It's nice
that the test runner uses reflection to determine automatically which tests to
run. (I'm used to such a thing with testing frameworks on Python.) It's also
nice that each test is run in its own domain meaning that silly mistakes like
dangling threads are easy to pick up on.

The final code is less tested than I'd like. Only writing the server-side
portion means that you're missing one of the ends for end-to-end testing.
That's not Windows' fault though.

# Documentation tools

I think the poor focus of Microsoft on documentation is particularly apparent
here. There is the most perfuctuary support for API documentation. Essentially
you can write arbitrary XML in a comment abover your method, class, etc
definition and have it concatenated together into an XML output file. There's
no HTML documentation tool built into Visual Studio and the solutions which
exist are clunky at best.

I suspect that the people at Microsoft think that code-completion is a
substitute for documentation.

# Continuous integration

I love [Travis CI](https://travis-ci.org/). Having a free service which will
observe a GitHub repository, check out any new commits and then try building
and testing your software in a fresh VM is wonderful. Having had to set up a
Jenkins server in a previous job I cannot tell you how nice it is to have a
system like Travis. It's brain-dead and simple but, like Unix, that is a
feature in itself. It's hard to do simple well and Travis does it excellently.

Travis CI only supports Linux test machines. (Or, at least, the free service
only support Linux.) That's not going to fly for Windows. Luckily someone
clearly saw a gap in the market and set up
[AppVeyor](http://www.appveyor.com/). It's not quite as nice as Travis but it's
also a lot younger. It's also not *quite* as simple to use but it *is*
opinionated. That means that you'll have a nice time if you don't fight the
"Windows way". A project which is laid out in the usual Visual Studio way will
Just Build (TM).

All of my external dependencies are either NuGet-able or are packaged as
re-distributable ``.msi`` instalers. After some Googling for the correct
PowerShell incantation, getting Bonjour and the Kinect SDKs auto-installing on
the test boxes was easy enough and the NuGet packages are downloaded
automatically by MSBuild.

I chose to have the non-NuGet dependencies in a [separate
repository](https://github.com/rjw57/streamkinect2.net-depends). Having big
binary blobs in your source repo is a Bad Idea. It's also a needless waste of
bandwidth for someone who clones your repo when they already have the
appropriate SDKs installed.

# Packaging

This is a little frustrating. For some reason, Microsoft saw fit to not ship
the support for packaging projects with the express edition of Visual Studio.
There is only support for publishing a "ClickOnce" package. It's OK as a
mechanism but I'm reserving judgement until I actually try to deploy this
software onto a separate machine.

# GUIs

The way that Windows Forms does GUI designing is a little dirty. I prefer a
more explicit separation between UI layout and logic. (WPF seems to be better
in that regard but, from what Googling I performed, it looks like WPF is a bit
of a dead-end for developing GUIs.) As it was, there would be the tiniest of
tiniest bits of GUI development for the server. I wanted most of the guts to
live in a library (or "assembly" in Micro-speak) and have the GUI basically be
a start/stop button and a log window. See below:

![]({{ site.url }}/images/streamkinect2-2014-09-17.png)

I'm a firm believer in separate modules and composable software and so the GUI
shell is just that: a shell. There's also a console version of the server in
the repository which is actually how I run it most of the time. Since there is
so little of it, having the GUI code be a bit ugly isn't a problem.

# Summary

If you are willing to do things the "Windows way" then writing software on
Windows is relatively painless. The packaging and dependency management story
is a lot better nowadays but it still is lacking far behind Linux. Debian has
had ``apt-get`` for over 15 years now and NuGet is not a lot better than
``apt`` was back then.

It's still too hard to set up a project in a way which encourages others to
build it; you need to jump through some hoops to lay it out in a way where your
development machine isn't special and NuGet is only a partial solution to
dependency hell. It is better than it was though and shows that the Microsoft
ecosystem is becoming a little more friendly to the "Open Source" model of
small projects shared widely.

Overall, I think this little experiment is a success and I'm well placed to
add actual real Kinect support to my code once the Windows 8 machine arrives.
With the CI system and GitHub, maybe I could even get a student to do it?

# Addendum: the problem

Below I'll describe the actual problem I was facing and why I decided to learn
an entirely new platform, new language and new IDE to solve it.

Firstly, a little context: this year I will have some Masters' degree students
working on a robotic project which hopes to use a [Microsoft Kinect for Windows
version 2](http://www.microsoft.com/en-us/kinectforwindows/) sensor. (This is
the one that comes with the XBox One console.) The project is a research
project and, to make life easier for the students, we will be using the
[ROS](http://www.ros.org/) to wire together the various algorithms we will be
using and to control the robot arm.

When using ROS, the path of least resistance is to use Ubuntu Linux.
While there are some very capable drivers for the original Kinect sensor, there
are unfortunately not currently any drivers for the Kinect version 2 sensor
which I consider stable enough to let students loose on. There is [a reverse
engineering effort](https://github.com/OpenKinect/libfreenect2) which may bear
fruit but, as of writing, it is not mature enough for our uses.

Being a fan of the simplest (a.k.a. "laziest") solution, I decided that it
would be best to have a dedicated Windows 8 computer with the Kinect plugged
into it. (This is proving a challenge, however, since any spare machines at
work tend to be running Linux. The number of Windows 8 machines is quite
small.) The computer would then stream the depth buffer into the rest of our
Linux-based pipeline. The precise nature of the research project means that
sub-100 millisecond latency isn't really required.

Similarly it isn't a requirement that the depth stream be completely
uncompressed. A quick back-of-envelope calculation reveals that a 1080p60
16-bit depth buffer is around 400 mega*bytes* per second. This is far more than
the network at work can deal with. Some brief experimentation showed that one
can non-linearly quantise a depth buffer to 8-bit precision using something
like the [μ-law algorithm](https://en.wikipedia.org/wiki/%CE%9C-law_algorithm)
and then compress it with JPEG in real-time to get the required bandwidth down
to a more manageable 1 or 2 megabytes per second.

All of this experimentation was done in Python and [the
code](https://github.com/rjw57/streamkinect2) is available if you want to take
a look. The experimental code also includes a simple client/server pair. The
server advertises itself over
[Zeroconf](https://en.wikipedia.org/wiki/Zero-configuration_networking) and
uses [ØMQ](https://en.wikipedia.org/wiki/%C3%98MQ) to stream depth frames over
the network. The idea being that we don't want to spend time configuring IPs,
subnet masks, etc, etc. Ideally we can just plug the Windows 8 machine into the
ROS machine with a network cable and "magic" will happen. Every required
configuration option is another potential point of failure.

So far, so good. All of the development at this point had been done in Linux
with Python and a little bit of code which mocked up the depth stream I'd be
getting from the Kinect. This allowed some rapid development and the ability to
[actually test](ttps://travis-ci.org/rjw57/streamkinect2) the client and server
bits by having the test suite start both on the same machine and provide a
"mock" Kinect device.

I was vaguely aware that the received opinion is that Python development on
Windows is a little hard but when I finally got around to finding a Windows box
to try installing the software on I found out how bad it was. Firstly, the
"official" Python is almost unusable. For anything other than the bleeding-edge
Python 3.4 release, installing simple tools like ``pip`` is a pain. Getting all
the pieces in line to actually ``pip install`` a C-backed module like
[pyzmq](https://zeromq.github.io/pyzmq/) is even worse. Continuum Analytics'
[Anaconda installer](http://continuum.io/downloads) makes life a lot easier but
it still requires quite an extensive amount of fiddling to get a machine set up
for development.

This goes against my natural inclination against "special snowflake" machines.
One of the advantages of having ``pip``-like tools in the first place is that
one can use generic VMs in the cloud to build-test your code on each commit.
Then you have an explicit, repeatable and automated recipe for turning your
GitHub repository into installed software. Having to set up a special
development machine will come back to haunt you the first time you need to get
someone else to build (or install) your software.
