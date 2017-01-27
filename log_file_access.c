#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// TODO: Generalize this to use directory name instead.
#define FILE_NAME "/tmp/data/test.csv"

/* Which means we should never try and monitor files under "/tmp". */
#define LOG_FILE "/tmp/file_accesses.log"

/**
 * Logs file accesses.
 *
 * TODO: Log PID, process name, and perhaps data that was read from the file?
 */
void log_file_access(const char *method, const char *path) {
  if (strcmp(path, FILE_NAME) != 0) {
    return;
  }

  // TODO: Use flock.
  FILE *fd = fopen(LOG_FILE, "a");

  if (fd != -1) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    unsigned long long milli_since_epoch =
        (unsigned long long)(tv.tv_sec) * 1000 +
        (unsigned long long)(tv.tv_usec) / 1000;

    fprintf(fd, "milli_since_epoch=\"%llu\",method=\"%s\",file=\"%s\"\n",
            milli_since_epoch, method, path);
  } else {
    fprintf(stderr, "Could not open access log file!\n");
  }

  fclose(fd);
}

/** Logs file accesses using a FILE descriptor instead of path. */
void log_file_access_from_FD(const char *method, FILE *fd) {
  // TODO:
  // http://stackoverflow.com/questions/11221186/how-do-i-find-a-filename-given-a-file-pointer
  log_file_access(method, "TODO: extract filename.");
}

/** Intercept fopen calls. */
FILE *fopen(const char *path, const char *mode) {
  log_file_access("fopen", path);

  static FILE *(*orig_func)();
  if (!orig_func) {
    orig_func = (FILE * (*)())dlsym(RTLD_NEXT, "fopen");
  }

  return orig_func(path, mode);
}

/** Intercept fopen64 calls. */
FILE *fopen64(const char *path, const char *mode) {
  log_file_access("fopen64", path);

  static FILE *(*orig_func)();
  if (!orig_func) {
    orig_func = (FILE * (*)())dlsym(RTLD_NEXT, "fopen64");
  }

  return orig_func(path, mode);
}

/** Intercept fwrite calls. */
size_t fwrite(const void *restrict ptr, size_t size, size_t nitems,
              FILE *restrict stream) {
  log_file_access_from_FD("fwrite", stream);

  static size_t *(*orig_func)();
  if (!orig_func) {
    orig_func = (size_t * (*)())dlsym(RTLD_NEXT, "fwrite");
  }

  return orig_func(ptr, size, nitems, stream);
}

/** Intercept fwrite64 calls. */
size_t fwrite64(const void *restrict ptr, size_t size, size_t nitems,
                FILE *restrict stream) {
  log_file_access_from_FD("fwrite64", stream);

  static size_t *(*orig_func)();
  if (!orig_func) {
    orig_func = (size_t * (*)())dlsym(RTLD_NEXT, "fwrite64");
  }

  return orig_func(ptr, size, nitems, stream);
}

/** Intercept fread calls. */
size_t fread(void *restrict ptr, size_t size, size_t nitems,
             FILE *restrict stream) {
  log_file_access_from_FD("fread", stream);

  static size_t *(*orig_func)();
  if (!orig_func) {
    orig_func = (size_t * (*)())dlsym(RTLD_NEXT, "fread");
  }

  return orig_func(ptr, size, nitems, stream);
}

/** Intercept fread64 calls. */
size_t fread64(void *restrict ptr, size_t size, size_t nitems,
               FILE *restrict stream) {
  log_file_access_from_FD("fread64", stream);

  static size_t *(*orig_func)();
  if (!orig_func) {
    orig_func = (size_t * (*)())dlsym(RTLD_NEXT, "fread64");
  }

  return orig_func(ptr, size, nitems, stream);
}

/** Intercept open calls. */
int open(const char *pathname, int flags, ...) {
  log_file_access("open", pathname);

  mode_t mode = 0;

  static int (*orig_func)();
  if (!orig_func) {
    orig_func = (int (*)())dlsym(RTLD_NEXT, "open");
  }

  if (flags & O_CREAT) {
    va_list arg;
    va_start(arg, flags);
    mode = va_arg(arg, mode_t);
    va_end(arg);
  }

  return mode == 0 ? orig_func(pathname, flags)
                   : orig_func(pathname, flags, mode);
}

/** Intercept open64 calls. */
int open64(const char *pathname, int flags, ...) {
  log_file_access("open64", pathname);

  mode_t mode = 0;

  static int (*orig_func)();
  if (!orig_func) {
    orig_func = (int (*)())dlsym(RTLD_NEXT, "open64");
  }

  if (flags & O_CREAT) {
    va_list arg;
    va_start(arg, flags);
    mode = va_arg(arg, mode_t);
    va_end(arg);
  }

  return mode == 0 ? orig_func(pathname, flags)
                   : orig_func(pathname, flags, mode);
}

/** Intercept read calls. */
// FIXME: Works only for Mac OS X.
ssize_t read(int fildes, void *buf, size_t nbytes) {
  log_file_access("read", "TODO: get filename.");

  static ssize_t (*orig_func)();
  if (!orig_func) {
    orig_func = (ssize_t(*)())dlsym(RTLD_NEXT, "read");
  }

  return orig_func(fildes, buf, nbytes);
}

/** Intercept read64 calls. */
// FIXME: Works only for Mac OS X.
ssize_t read64(int fildes, void *buf, size_t nbytes) {
  log_file_access("read64", "TODO: get filename.");

  static ssize_t (*orig_func)();
  if (!orig_func) {
    orig_func = (ssize_t(*)())dlsym(RTLD_NEXT, "read64");
  }

  return orig_func(fildes, buf, nbytes);
}

/** Intercept write calls. */
// FIXME: Works only for Mac OS X.
ssize_t write(int fildes, const void *buf, size_t nbytes) {
  log_file_access("write", "TODO: get filename.");

  static ssize_t (*orig_func)();
  if (!orig_func) {
    orig_func = (ssize_t(*)())dlsym(RTLD_NEXT, "write");
  }

  return orig_func(fildes, buf, nbytes);
}

/** Intercept write64 calls. */
// FIXME: Works only for Mac OS X.
ssize_t write64(int fildes, const void *buf, size_t nbytes) {
  log_file_access("write64", "TODO: get filename.");

  static ssize_t (*orig_func)();
  if (!orig_func) {
    orig_func = (ssize_t(*)())dlsym(RTLD_NEXT, "write64");
  }

  return orig_func(fildes, buf, nbytes);
}
