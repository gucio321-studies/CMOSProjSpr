#!/bin/bash
# This script converts content of your current Ctrl+C-clipboard, which is supposed
# to be a table copied from LibreOffice Calc, into a markdown table format.
# Output is stored in your middle-click-clipboard.
xclip -selection clipboard |sed -e 's/\t\+/ | /g' -e 's/^/| /' -e 's/$/ |/g' |xclip
