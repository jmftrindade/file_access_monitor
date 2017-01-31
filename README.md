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

# Alternative: Using loggedfs instead to monitor file accesses.

1. Install http://github.com/jmftrindade/loggedfs  (Tested on linux; Mac OS X doesn't work because of libfuse incompatibility)

2. Run loggedfs, e.g., monitor all files under home directory:

```
loggedfs -c loggedfs.xml -l /var/tmp/$USER-home-fs.log ~
```

Output will be at /var/tmp/$USER-home-fs.log

3. Disable loggedfs, e.g., assuming monitoring was configured to track home directory:

```
sudo umount -l ~
```
