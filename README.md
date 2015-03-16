remora
======

Like its namesake, the remora module is like a small, annoying parasite stuck
to the underside of [AWSCLI](https://aws.amazon.com/cli).

The main purpose of remora is to allow you to use all of the great
functionality of AWSCLI programmatically as a library.  It does this by hacking
into internal, private interfaces of AWSCLI in a way that is:

* Not particularly well thought out
* Not well-tested
* Almost guaranteed to break in the future
* Not supported in any way by the AWSCLI team

You really shouldn't use this library.  Really.

Usage
-----

If you were not scared off by anything above you really should be.  But here's
how you would use remora.

    import remora

    cli = remora.cli()
    data = cli('ec2 describe-instances')

The variable data would now contain the full contents of the data returned by
the underlying [botocore](https://github.com/boto/botocore) call as a Python
dictionary.

Or, perhaps you would like to use the nifty multi-part download feature of the
``s3`` client.  You could do this:

    data = cli('s3 cp s3://mybucket/my_ginormous_file .')

And your ginormous file would be efficiently downloaded in parts to the current
directory.

Basically, any command you can run in AWSCLI should be available via remora.
Just leave off the initial ``aws `` part of the command.

Caveats
-------

A few (additional) caveats:

* The ``--profile`` option does not work properly since the botocore session
  object is retained across commands.  If you want to use a particular profile
  pass that in to the call to ``remora.cli(profile='foobar')``.  If you need to
  use different profiles, create multiple ``cli's``.
* Some customized commands in AWSCLI (e.g. ``s3 ls``) do not return data but
  simply print information to stdout.  This information will be printed but
  will not be returned in a Python data structure.
