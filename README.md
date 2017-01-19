# file_access_monitor
Utility to monitor file accesses for any files in a set of directories.

# Build
```
make
```

# Instrument a specific binary
Watch for events on log file:
```
touch /tmp/file_accesses.log
tail -f /tmp/file_accesses.log &
```

## Sample binary instrumentation
Linux:
```
LD_PRELOAD=./log_file_access.o ./write_test.sh
```

Mac OS X:
```
DYLD_FORCE_FLAT_NAMESPACE=1 DYLD_INSERT_LIBRARIES=./log_file_access.dylib ./write_test.sh
```
