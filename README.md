This is a quick script to convert notes from Tomboy to Evernote.

This project was dervied from @scribu's work (cited below), but this one makes a best-effort pass to convert Tomboy markup to standard HTML compatible with Evernote's ENML, whereas @scribu's would drop most formatting markup.


### Usage

Whereas @scribu's required external dependencies, this one relies on standard Python modules:

- xml.dom.minidom
- re
- datetime

This one also requires _you_ to select which Tomboy notes you want to export, and writes them all to standard output.

```shell
# Export **all** Tomboy notes in your home directory
find $HOME -type f -name '*.note' -print0 | xargs -0 trombone > EXPORT.enex
```

Note that on Mac OS X, Tomboy's notes are stored in:

- `$HOME/Library/Application\ Support/Tomboy/`

On Linux, it's usually

- `$HOME/.local/share/tomboy/`


### Limitations

- None! (that I know of)


### Resources

- <https://gist.github.com/scribu/7442170> (Thanks @scribu)
- <https://gist.github.com/chrishan/3186646> (Thanks @chrishan)
- <https://blog.evernote.com/tech/2013/08/08/evernote-export-format-enex/>
- <http://dev.evernote.com/doc/articles/enml.php>
- <https://wiki.gnome.org/Apps/Tomboy/NoteXmlFormat>
