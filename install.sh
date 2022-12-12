#!/bin/bash
INSTALLDIR="/usr/local/bin"

[ -f randrn.py ] && sudo cp --remove-destination randrn.py "$INSTALLDIR" || echo "randrn.py not found! Where are we running this from?"