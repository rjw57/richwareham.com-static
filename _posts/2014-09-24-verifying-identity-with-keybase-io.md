---
title: Verifying identity on social media with keybase.io and command-line tools
cover: images/security-pass.jpg
---

I recently joined [keybase.io](https://keybase.io) which is an interesting
experiment in verifiable assertions of identity on social media. The concept is
simple: if I tweet [a
message](https://twitter.com/richwareham/status/514478671852089346) which can
be verified as being signed by my private key then you can trust that, at that
point, my twitter account was controlled by someone who also had access to my
private key. The same assertions can be made about GitHub accounts by signing
[a gist](https://gist.github.com/rjw57/f2f7b7b2da6ed3cc149c) which makes a
similar statement.

Assuming that one trusts a user to be savvy enough to revoke these assertions
if they believe their private key is compromised, this provides a fairly strong
assertion that various social media accounts are controlled by the same entity.
Of course one could do this already oneself using
[GPG](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) but keybase.io provides
a relatively nice workflow and a pretty website. Do not underestimate the
advantages which this can bring.

# Why is this useful?

I must admit that I do not have a long list of reasons why it is useful to tie
social media account identities together and associate them with a public key
apart from it being a sort of social media "verified tick" which is available
to anyone.

That being said, there are a few use cases I can think of. If one is a software
developer which makes signed releases but is otherwise anonymous, e.g.
TrueCrypt, then it would be useful to assert that a twitter account is
controlled by the same person. To flip this in the other direction, if you know
that a Twitter account is controlled by someone with access to a private key
then you can have some confidence that anything signed by that private key came
from the same person. Finally, it's useful to be able to say that
``@john_q_rockstar`` on Twitter is the same as the person running
``https://johnqrockstar.com/`` without relying on there being a Twitter
"verified" tick.

# So, how does it work?

The central keybase.io concept is that one should be able to verify for oneself
that a social media account or DNS domain was at some point controlled by
someone in possession of the private half of a public key which you trust.
Let's work through an example of verifying that [my public
key](https://pgp.mit.edu/pks/lookup?op=vindex&search=0x7BA6A2C74E3D7E0D) is
associated with ``richwareham.com``. (Note that
[DNSSEC](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions)
does not solve this exact problem although it certainly works in a related
space.)

It would be nice to be able to verify ``richwareham.com`` without trusting
keybase.io infrastructure to actually do the verification. In that way,
keybase.io can be seen as a nice tool for creating the verifications without
being a critical, or trusted, component in the chain.

## Importing the public key

The first thing that one needs to do is to import my public key. Obviously I
already have mine imported but one can always import it again:

```console
$ curl -s https://keybase.io/richwareham/key.asc | gpg --import
gpg: key 4E3D7E0D: "Rich Wareham (Personal) <rjw57@cantab.net>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
```

Let's just check the fingerprint of that key:

```console
$ gpg --fingerprint rjw57@cantab.net
pub   4096R/4E3D7E0D 2011-10-12
      Key fingerprint = 4E27 6278 B082 CE98 E5A9  618E 7BA6 A2C7 4E3D 7E0D
uid                  Rich Wareham (Personal) <rjw57@cantab.net>
sub   4096R/4D4C8881 2011-10-12
```

This fingerprint can be verified against both my [keybase.io profile
page](https://keybase.io/richwareham) and the [MIT public key
server](https://pgp.mit.edu/pks/lookup?op=vindex&search=0x7BA6A2C74E3D7E0D). It
should also appear in your web of trust if you have any trust in the keys which
signed mine.

## Getting the assertion from DNS

We now need to see what is asserted in DNS. We can use the ``dig`` tool to get
any ``TXT`` records from ``richwareham.com``:

```console
$ dig txt richwareham.com | grep keybase
richwareham.com.        7687    IN      TXT     "keybase-site-verification=AnLTOBDGpT9Efr0DJn4X4C7VcnwZF_ZRT6Vx8_pk_J8"
```

The important record here is the one containing ``keybase-site-verification``.
This also contains the following apparently magic string:

> AnLTOBDGpT9Efr0DJn4X4C7VcnwZF_ZRT6Vx8_pk_J8

## What the assertion actually is

On the [associated proof
page](https://keybase.io/richwareham/sigs/AnLTOBDGpT9Efr0DJn4X4C7VcnwZF_ZRT6Vx)
for my DNS assertion you can see a walk through of how that magic string was
generated. It indicates that everything started from a JSON-formatted assertion
message which was signed by my public key. Let's use GPG to verify that by
pasting in the GPG signed statement from the website:

```console
$ gpg <<EOL
> -----BEGIN PGP MESSAGE-----
> Version: GnuPG v1
> 
> owGbwMvMwMRYvWzRcT/bOl7G0we+JDGEKO5kqVZKyk+pVLKqVspOBVNpmXnpqUUF
> RZl5JUpWSiapRuZmRuYWSQYWRsmplhappomWZoYWqeZJiWaJRsnmJqnGKeapBilK
> OkoZ+cUgHUBjkhKLU/Uy84FiQE58ZgpQFIv6UoiEiXmqRaqFgaGhhWGyibmxqbmx
> iXmyWaKZmZm5oYmBAUhhcWpRXmJuKlB1UWZyRnliUWpGYq5SrY4SUKIsMzkV5OyU
> /NzEzDxUJXrJ+blA/QVF+SX5yfk5QMmUvGKQvpLKApBp5alJ8VAj4pMy81KAPgcq
> L0stKs7MBxplCFSZXJIJstjQxNDQBOhxSyMdpdSKgsyi1HiQZYam5mYWBkAAsiS1
> DGikAdAzZqmJhsaJyZbmqWlmZmmmiYaWyQZJaeYmKSlJySYmaSlJxkZmJolGaQZJ
> RkmJiUkGBqYGlompBubGFoapSiBPFeblK1kZA52ZmA40sjgzPS+xpLQoVamWq5NJ
> hoWBkYmBjZUJFHkMXJwCsChVOsz/z7JYubSvKVrRcRKfrdRDrYenTvLc9vr2fcnq
> VPuHGeuV2apPxnP94vM3PZcRKCjfH7rxo4PY89Iz0xZ5HLPdpfPgtimHy5u+jZ+i
> JbjWn3WyUVz1o+73Kle7oN/FJgXuERN+ap7mddU1M5Y5+3j2ujkznPW63Jbedb5V
> 4129ke9m563VRyMvPeVYfUhfo3zzzxBxUTmFtfsP/ou5qfBv+R9TC83jry+39WvL
> mqrf/r9j93Zln+6QS1kc3qveahSzyy7426Jx/cDpW/POPqhnXvVRt9OtwbvM686c
> 3La7lXOOci7L0XpgnB+9PlE9ztk9SfpK3JZfrtMLV32fkKn80XRS3T7fg0Lvgk88
> zjLwy11SeGT+z9mtmo8ebJubUnDnw4IghdT5fr9DZ8w/p3Sc+2Tcct7NTkInxaUZ
> HfQy3wVPvVpvWFWlHPn/1fSiYz+ynpnfUZ+wq/nhy05rU/np3IcMze8cO/V60ctl
> By7xlTqYmqVYndve7bxLZV1TKP86s/1aCxYwf31//d3a/a9VG+7t7is8KpmTIuC3
> I7egrTU7M7ajOnfO7xNbLlo48H0Ta70yb5q33IV5/NtrK2Q0OHv23/fRl/IL3KXy
> uWHBuxZHWavSiXZPTKzY9D3fy+yZ2mWl3STNs3fJvpv/dqqF5kytS1t7esYu9oqX
> Z39fWa/svfjzQpcLwR5652bfvGBixnb+YG5J7B+hWWX1lwE=
> =bND4
> -----END PGP MESSAGE-----
> EOL
{"body":{"key":{"fingerprint":"4e276278b082ce98e5a9618e7ba6a2c74e3d7e0d","host":"keybase.io","key_id":"7ba6a2c74e3d7e0d","uid":"747e8e801181c47357347c6a66671400","username":"richwareham"},"service":{"domain":"richwareham.com","protocol":"dns"},"type":"web_service_binding","version":1},"ctime":1411496192,"expire_in":157680000,"prev":"0e8e6ea13ac97ef66f5a19c0bf74ddbc44fdb3264a2f0b2baab00509ae07381e","seqno":3,"tag":"signature"}
gpg: Signature made Tue 23 Sep 2014 19:16:36 BST using RSA key ID 4E3D7E0D
gpg: Good signature from "Rich Wareham (Personal) <rjw57@cantab.net>"
```

Indeed this is a message signed by my key. The message includes a fingerprint
of my public key, my keybase.io username, the DNS domain I was asserting is
mine and when I made the assertion. OK so I trust that I actually asserted once
that I control ``richwareham.com``. But I could just as easily assert I control
``google.com``. We need to use the TXT record on ``richwareham.com`` to
actually check this.

## Getting the expected hash

The next stage is to take the actual signed message and compute a
[SHA-256](https://en.wikipedia.org/wiki/SHA-2) hash of its binary
representation. Fortunately that's pretty easy. Stripped of the header and
footer, a GPG message is just a
[Base64](https://en.wikipedia.org/wiki/Base64)-encoded binary blob. We can use
the ``base64`` utility to decode it, the ``sha256sum`` utility to compute the
SHA-256 hash of the contents and then use the ever-wonderful ``xxd`` utility to
convert the hex-string produced by ``sha256sum`` into a binary file containing
the 256-bits (or 32-bytes) of hash:

```console

$ base64 -d << EOL | sha256sum - | xxd -r -p expected.bin
> owGbwMvMwMRYvWzRcT/bOl7G0we+JDGEKO5kqVZKyk+pVLKqVspOBVNpmXnpqUUF
> RZl5JUpWSiapRuZmRuYWSQYWRsmplhappomWZoYWqeZJiWaJRsnmJqnGKeapBilK
> OkoZ+cUgHUBjkhKLU/Uy84FiQE58ZgpQFIv6UoiEiXmqRaqFgaGhhWGyibmxqbmx
> iXmyWaKZmZm5oYmBAUhhcWpRXmJuKlB1UWZyRnliUWpGYq5SrY4SUKIsMzkV5OyU
> /NzEzDxUJXrJ+blA/QVF+SX5yfk5QMmUvGKQvpLKApBp5alJ8VAj4pMy81KAPgcq
> L0stKs7MBxplCFSZXJIJstjQxNDQBOhxSyMdpdSKgsyi1HiQZYam5mYWBkAAsiS1
> DGikAdAzZqmJhsaJyZbmqWlmZmmmiYaWyQZJaeYmKSlJySYmaSlJxkZmJolGaQZJ
> RkmJiUkGBqYGlompBubGFoapSiBPFeblK1kZA52ZmA40sjgzPS+xpLQoVamWq5NJ
> hoWBkYmBjZUJFHkMXJwCsChVOsz/z7JYubSvKVrRcRKfrdRDrYenTvLc9vr2fcnq
> VPuHGeuV2apPxnP94vM3PZcRKCjfH7rxo4PY89Iz0xZ5HLPdpfPgtimHy5u+jZ+i
> JbjWn3WyUVz1o+73Kle7oN/FJgXuERN+ap7mddU1M5Y5+3j2ujkznPW63Jbedb5V
> 4129ke9m563VRyMvPeVYfUhfo3zzzxBxUTmFtfsP/ou5qfBv+R9TC83jry+39WvL
> mqrf/r9j93Zln+6QS1kc3qveahSzyy7426Jx/cDpW/POPqhnXvVRt9OtwbvM686c
> 3La7lXOOci7L0XpgnB+9PlE9ztk9SfpK3JZfrtMLV32fkKn80XRS3T7fg0Lvgk88
> zjLwy11SeGT+z9mtmo8ebJubUnDnw4IghdT5fr9DZ8w/p3Sc+2Tcct7NTkInxaUZ
> HfQy3wVPvVpvWFWlHPn/1fSiYz+ynpnfUZ+wq/nhy05rU/np3IcMze8cO/V60ctl
> By7xlTqYmqVYndve7bxLZV1TKP86s/1aCxYwf31//d3a/a9VG+7t7is8KpmTIuC3
> I7egrTU7M7ajOnfO7xNbLlo48H0Ta70yb5q33IV5/NtrK2Q0OHv23/fRl/IL3KXy
> uWHBuxZHWavSiXZPTKzY9D3fy+yZ2mWl3STNs3fJvpv/dqqF5kytS1t7esYu9oqX
> Z39fWa/svfjzQpcLwR5652bfvGBixnb+YG5J7B+hWWX1lwE=
> EOL
$ hexdump -C expected.bin
00000000  02 72 d3 38 10 c6 a5 3f  44 7e bd 03 26 7e 17 e0  |.r.8...?D~..&~..|
00000010  2e d5 72 7c 19 17 f6 51  4f a5 71 f3 fa 64 fc 9f  |..r|...QO.q..d..|
00000020
```

Now we have a file, ``expected.bin``, which contains a 256 bit (32 byte) hash
of our signed assertion. To prove that I control ``richwareham.com``, I
added a TXT record which contained an encoded form of that hash.

## Getting the actual hash from DNS

It's asserted that the magic string we found in the DNS TXT record should be
the web-safe Base64 encoding of that very hash. The assumption being that only
someone in control of the domain would be able to insert a TXT record which is
cryptographically equivalent to their assertion of control.

Web-safe Base64 is just normal Base64 with ``+`` and ``/`` replaced with ``-``
and ``_``. We can use the Unix ``tr`` utility to swap those characters and
decode the Base64.

```console
$ echo 'AnLTOBDGpT9Efr0DJn4X4C7VcnwZF_ZRT6Vx8_pk_J8' | tr -- -_ +/ | base64 -d >actual.bin
base64: invalid input
$ hexdump -C actual.bin 
00000000  02 72 d3 38 10 c6 a5 3f  44 7e bd 03 26 7e 17 e0  |.r.8...?D~..&~..|
00000010  2e d5 72 7c 19 17 f6 51  4f a5 71 f3 fa 64 fc 9f  |..r|...QO.q..d..|
00000020
```

The ``invalid input`` warning here can be ignored since it relates to a missing
``=`` character on the end of the hash used to indicate the correct padding.
If you are concerned, you can verify that appending an ``=`` to the hash
removes the warning.

## Comparing the hashes

We could manually compare the hex-dumps from the expected and actual hashes but
there exists a utility whose sole purpose is to compare files so let's use it:

```console
$ diff -s actual.bin expected.bin
Files actual.bin and expected.bin are identical
```

The hashes match and so we may conclude that I have once had control of
``richwareham.com``.

# Summary

I'm not sure if keybase.io will take off as a concept but it's a nice idea. The
technology to cryptographically assert control over social media accounts has
existed for some time but keybase.io wraps it up into a nice bundle. They also
have some rather spiffy little web-tools which allow one to verify messages
from people you follow (or "track") on keybase.io and, if one trusts their
Javascript crypto, you can even host an encrypted private key with them.

I already have a GPG key and I'd rather not upload it, even encrypted, to a
random website. Recognising this, the entire keybase verification workflow can
be done client-side on your machine using GPG. Although I signed the assertions
of control hosted on keybase.io, I did so on my machine using GPG without ever
sending the private key to them. This is the key advantage of public key
cryptosystems and so it's nice to see keybase.io supporting this.

I'm still waiting to see what the killer use-case for it will turn out to be.

