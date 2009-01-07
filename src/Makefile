libtics.so : draw.o fitness.o
	ld -shared -o libtics.so draw.o fitness.o

draw.o : draw.c
	cc -c -o draw.o draw.c

fitness.o : fitness.c
	cc -c -o fitness.o fitness.c

install : libtics.so
	install -m 644 libtics.so /usr/local/lib

clean:
	rm -f *.o *.so
