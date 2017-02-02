# Run demo:

```
jupyter notebook lineage_graph_with_py2neov3.ipynb
```

# Using loggedfs to monitor file accesses.

1. Install http://github.com/jmftrindade/rlog (Tested on linux Ubuntu 16.04)

2. Install http://github.com/jmftrindade/loggedfs  (Tested on linux; Mac OS X doesn't work because of OSX libfuse incompatibility)

3. Run loggedfs, e.g., monitor all files under home directory:

```
LD_LIBRARY_PATH=/usr/local/lib loggedfs -c loggedfs.xml -l /var/tmp/$USER-home-fs.log ~
```

Output will be at /var/tmp/$USER-home-fs.log

3. Disable loggedfs, e.g., assuming monitoring was configured to track home directory:

```
sudo umount -l ~
```

4. Copy events log to this directory, in case you want to use that for the demo:

```
cp /var/tmp/$USER-home-fs.log loggedfs_events_log.csv
```

# DEPRECATED:

Started out with a dynamic instrumentation module, which worked fine with (f)open and (f)close events, but for some reason (f)read and (f)write are not getting intercepted.  Abandoned this in favor of custom fork of loggedfs FUSE lib.

## file_access_monitor
Utility to monitor file accesses for any files in a set of directories.

## Build
```
make
```

## Instrument a specific binary
Watch for events on log file:
```
touch /tmp/file_accesses.log
tail -f /tmp/file_accesses.log &
```

### Sample binary instrumentation
Linux:
```
LD_PRELOAD=./log_file_access.o ./test_workflows/copy_file_via_cp.sh
```

Mac OS X:
```
DYLD_FORCE_FLAT_NAMESPACE=1 DYLD_INSERT_LIBRARIES=./log_file_access.dylib ./test_workflows/copy_file_via_cp.sh
```
