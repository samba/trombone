from setuptools import setup

VERSION="0.1"

try:
    long_description=open('DESCRIPTION.rst', 'rt').read()
except Exception:
    long_description="Export notes from Tomboy to Evernote"



setup(
    name = "trombone",
    description = "Export notes from Tomboy to Evernote",
    long_description = long_description,

    version = VERSION,

    author = 'Sam Briesemeister',
    author_email = 'sam.briesemeister@gmail.com',

    url = 'https://github.com/samba/trombone',
    download_url = "https://github.com/samba/trombone/tarball/" + VERSION,

    license = 'GPL',
    packages = ["Evernote", "Tomboy"],
    scripts = ["trombone"],

    zip_safe = True
)
