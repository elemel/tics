OBJ=	tics.o clamp.o Image.o Triangle.o Vertex.o
LDFLAGS=	-lGL -lSDL -lSDL_image

tics : $(OBJ)
	g++ -o tics $(OBJ) $(LDFLAGS)

tics.o : tics.cpp Image.hpp
	g++ -c -o tics.o tics.cpp

clamp.o : clamp.cpp clamp.hpp
	g++ -c -o clamp.o clamp.cpp

Image.o : Image.cpp Image.hpp
	g++ -c -o Image.o Image.cpp

Triangle.o : Triangle.cpp Triangle.hpp
	g++ -c -o Triangle.o Triangle.cpp

Vertex.o : Vertex.cpp Vertex.hpp clamp.hpp
	g++ -c -o Vertex.o Vertex.cpp

install : tics
	install -m 755 tics /usr/local/bin

Image.hpp : Triangle.hpp
	touch Image.hpp

Triangle.hpp : Vertex.hpp
	touch Triangle.hpp

clean:
	rm -f tics *.o
