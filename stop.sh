timecode=$(date +%Y.%m.%d-%H.%M.%S)
cd logs
mv latest.log $timecode.log
mv latest.error.log $timecode.error.log
xz $timecode.log
xz $timecode.error.log
