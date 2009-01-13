libtics.so : fitness.o
	ld -shared -o libtics.so fitness.o

fitness.o : fitness.c
	cc -c -o fitness.o fitness.c

install : libtics.so
	install -m 644 libtics.so /usr/local/lib

clean:
	rm -f *.o *.so
