# v1.1 — Update Log

## what's new

- full Linux and macOS compatibility
  - fixed stdout encoding issues on all platforms
  - unicode fallback for terminals that can't display special characters
  - fixed Ctrl+C handling on Linux and macOS
  - all file reads and writes now use utf-8 encoding

- custom .txt file support
  - load your own list of usernames from any .txt file
  - one username per line, lines starting with # are ignored
  - works on all platforms

- estimated time remaining
  - shows live eta on the status line while checking
  - formats as seconds, minutes or hours automatically

- retry option
  - after checking finishes it asks if you want to run again
  - no need to restart the script — picks new settings each run
  - fixed recursion issue from v1.0 that could crash on many retries

- max 1 underscore per username
  - fixed generator to never produce names with 2+ underscores

- added 3-letter username support

- version bump to 1.1
