all : libtics_draw.so libtics_fitness.so

libtics_draw.so : draw.o
	ld -shared -o libtics_draw.so draw.o

libtics_fitness.so : fitness.o
	ld -shared -o libtics_fitness.so fitness.o

draw.o : draw.c
	cc -c -o draw.o draw.c

fitness.o : fitness.c
	cc -c -o fitness.o fitness.c

clean:
	rm -f *.o *.so
