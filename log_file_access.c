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

    fprintf(fd, "milli_since_epoch=\"%llu\",method=\"%s\",file=\"%s\"\n", milli_since_epoch, method, path);
  } else {
    fprintf(stderr, "Could not open access log file!\n");
  }

  fclose(fd);
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
