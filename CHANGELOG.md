# Changelog

## 0.6.0
- Modernized runtime for Python 3.
- Added optional web UI mode for running scanner jobs.
- Reduced hard dependency on platform-specific modules (readline/psutil/termcolor) so the CLI can start on more environments.
- Reworked sniffer module to a minimal Python 3-compatible implementation.
- Disabled the legacy DoS module implementation in this build due to severe runtime breakage.

## 0.5.8
- Legacy release (original upstream baseline).
