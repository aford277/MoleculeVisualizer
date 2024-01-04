CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: mol.o libmol.so molecule_wrap.c molecule_wrap.o _molecule.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

molecule_wrap.c: molecule.i
	swig -python molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I /usr/include/python3.7 -o molecule_wrap.o

_molecule.so: molecule_wrap.o
	$(CC) molecule_wrap.o -shared -lpython3.7 -lmol -dynamiclib -L. -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -o _molecule.so

clean:
	rm -f *.o *.so
