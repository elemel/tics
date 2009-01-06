libtics_fitness.so : fitness.o
	ld -shared -o libtics_fitness.so fitness.o

fitness.o : fitness.c
	cc -c -o fitness.o fitness.c

clean:
	rm -f fitness.o libtics_fitness.so
