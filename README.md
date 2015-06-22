# ghi-assist
Bot that organizes Github Issues!

Out of the box functionality is as follows:

**Assign Related Issue:** When a PR is submitted with a comment saying it fixes a particular issue, assign that issue to the user that submitted the PR.

**Claim Issue:** If a user submits a comment on the issue saying "claim" "claiming" or "claimed", assign the issue to that user unless it is already assigned to someone else.

**Add Labels:** When opening or commenting on an issue or PR, any lines beginning with '##' will be scanned for the names of any labels, and if found, applied to the issue or PR.  Labels must be defined in `etc/config.json` to be considered valid.


## Installation
    (virtualenv preferred)
    python setup.py install

## Tests
    py.test tests

## Running

### Configuration
Sample configuration is provided in `etc/config/sample.json`.

    cp etc/config.sample.json etc/config.json

### Usage
    python bin/server.py
