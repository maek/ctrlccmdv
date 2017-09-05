Ctrl-c cmd-v
============

This is a simple daemon written in Python 2 that allows text in the clipboard to
be shared between two remote hosts simply via `Ctrl-c` `Ctrl-v`.

Supported OS:

- Linux (GNOME only)
- macOS

NOTE: There is no encryption so all communications are sent as clear text.


Run Instructions
----------------

To start the daemon:

```bash
$ ./ctrlccmdv.py <HOST> &
```

To stop the daemon:

```bash
$ pkill -f ctrlccmdv.py >/dev/null
```
