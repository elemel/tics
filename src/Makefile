LD=			$(CXX)
OBJS=		clamp.o Image.o io.o Pixels.o Random.o tics.o Triangle.o Vertex.o
CXXFLAGS=	-Wall -g
LDFLAGS=	-lGL -lSDL -lSDL_image

default : tics

tics : $(OBJS)
	$(LD) -o tics $(OBJS) $(LDFLAGS)

clamp.o : clamp.cpp clamp.hpp

Image.o : Image.cpp Image.hpp io.hpp Random.hpp

io.o : io.cpp io.hpp

Pixels.o : Pixels.cpp Pixels.hpp

Random.o : Random.cpp Random.hpp

tics.o : tics.cpp Image.hpp Pixels.hpp Random.hpp

Triangle.o : Triangle.cpp Triangle.hpp Random.hpp

Vertex.o : Vertex.cpp Vertex.hpp clamp.hpp io.hpp Random.hpp

Image.hpp : Triangle.hpp
	touch Image.hpp

Triangle.hpp : Vertex.hpp
	touch Triangle.hpp

install : tics
	install -m 755 tics /usr/local/bin

clean:
	rm -f tics *.o
