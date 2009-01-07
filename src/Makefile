OBJ=	clamp.o Image.o Pixels.o random.o tics.o Triangle.o Vertex.o
LDFLAGS=	-lGL -lSDL -lSDL_image

default : tics

tics : $(OBJ)
	g++ -o tics $(OBJ) $(LDFLAGS)

clamp.o : clamp.cpp clamp.hpp
	g++ -c -o clamp.o clamp.cpp

Image.o : Image.cpp Image.hpp
	g++ -c -o Image.o Image.cpp

Pixels.o : Pixels.cpp Pixels.hpp
	g++ -c -o Pixels.o Pixels.cpp

random.o : random.cpp random.hpp
	g++ -c -o random.o random.cpp

Triangle.o : Triangle.cpp Triangle.hpp
	g++ -c -o Triangle.o Triangle.cpp

Vertex.o : Vertex.cpp Vertex.hpp clamp.hpp random.hpp
	g++ -c -o Vertex.o Vertex.cpp

tics.o : tics.cpp Image.hpp
	g++ -c -o tics.o tics.cpp

Image.hpp : Triangle.hpp
	touch Image.hpp

Triangle.hpp : Vertex.hpp
	touch Triangle.hpp

install : tics
	install -m 755 tics /usr/local/bin

clean:
	rm -f tics *.o
