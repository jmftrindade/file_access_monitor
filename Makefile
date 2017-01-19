# To instrument a binary:
#
# Mac OS X:
# DYLD_FORCE_FLAT_NAMESPACE=1 DYLD_INSERT_LIBRARIES=./log_file_access.dylib ./my_binary
#
# Linux:
# LD_PRELOAD=./log_file_access.o ./my_binary

log_file_accesses.s:
	# Linux:
	#gcc -std=c99 -Wall -shared -fPIC log_file_access.c -o log_file_access.so -ldl
	# Mac OS X:
	gcc -std=c99 -Wall -fPIC -dynamiclib -o log_file_access.dylib -dy log_file_access.c

clean:
	rm *.so
