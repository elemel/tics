OBJ=	tics.o Byte.o Image.o Triangle.o Vertex.o
LDFLAGS=	-lGL -lSDL -lSDL_image

tics : $(OBJ) Image.hpp
	g++ -o tics $(OBJ) $(LDFLAGS)

tics.o : tics.cpp
	g++ -c -o tics.o tics.cpp

Byte.o : Byte.cpp Byte.hpp
	g++ -c -o Byte.o Byte.cpp

Image.o : Image.cpp Image.hpp
	g++ -c -o Image.o Image.cpp

Triangle.o : Triangle.cpp Triangle.hpp
	g++ -c -o Triangle.o Triangle.cpp

Vertex.o : Vertex.cpp Vertex.hpp
	g++ -c -o Vertex.o Vertex.cpp

install : tics
	install -m 755 tics /usr/local/bin

Image.hpp : Triangle.hpp
	touch Image.hpp

Triangle.hpp : Vertex.hpp
	touch Triangle.hpp

Vertex.hpp : Byte.hpp
	touch Vertex.hpp

clean:
	rm -f tics *.o
