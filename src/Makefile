LD=			$(CXX)
OBJS=		clamp.o Image.o Pixels.o random.o tics.o Triangle.o Vertex.o
CXXFLAGS=	-Wall -DNDEBUG -O9
LDFLAGS=	-lGL -lSDL -lSDL_image

default : tics

tics : $(OBJS)
	$(LD) -o tics $(OBJS) $(LDFLAGS)

clamp.o : clamp.cpp clamp.hpp

Image.o : Image.cpp Image.hpp

Pixels.o : Pixels.cpp Pixels.hpp

random.o : random.cpp random.hpp

tics.o : tics.cpp Image.hpp

Triangle.o : Triangle.cpp Triangle.hpp

Vertex.o : Vertex.cpp Vertex.hpp clamp.hpp random.hpp

Image.hpp : Triangle.hpp
	touch Image.hpp

Triangle.hpp : Vertex.hpp
	touch Triangle.hpp

install : tics
	install -m 755 tics /usr/local/bin

clean:
	rm -f tics *.o
