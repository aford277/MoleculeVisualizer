import molecule

header = """<svg version="1.1" width="1200" height="1600"
xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500

class Atom:
    # initializes the Atom
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z

    # returns a string with the values in the Atom to debug
    def __str__(self):
        return "Element: %s x: %lf y: %lf z: %lf\n" % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z)

    # returns a string containing the details of the Atom to add to an svg file
    def svg(self):
        x100 = self.c_atom.x * 100.0 + offsetx
        y100 = self.c_atom.y * 100.0 + offsety
        if(self.c_atom.element in radius and self.c_atom.element in element_name):
            return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x100, y100, radius[self.c_atom.element], element_name[self.c_atom.element])
        else:
            return '  <circle cx="%.2f" cy="%.2f" r="40" fill="url(#default)"/>\n' % (x100, y100)

class Bond:
    # initializes the Bond
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.z = c_bond.z

    # returns a string with the values in the Bond to debug
    def __str__(self):
        return "a1: %d a2: %d epairs: %d x1: %lf y1: %lf x2: %lf y2: %lf len: %lf dx: %lf dy: %lf z: %lf\n" % (self.c_bond.a1, self.c_bond.a2, self.c_bond.epairs, self.c_bond.x1, self.c_bond.y1, self.c_bond.x2, self.c_bond.y2, self.c_bond.len, self.c_bond.dx, self.c_bond.dy, self.c_bond.z)

    # returns a string containing the details of the Bond to add to an svg file
    def svg(self):
        x1_100 = self.c_bond.x1 * 100.0 + offsetx
        x2_100 = self.c_bond.x2 * 100.0 + offsetx
        y1_100 = self.c_bond.y1 * 100.0 + offsety
        y2_100 = self.c_bond.y2 * 100.0 + offsety
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1_100 + self.c_bond.dy*10, y1_100 - self.c_bond.dx*10, x1_100 - self.c_bond.dy*10, y1_100 + self.c_bond.dx*10, x2_100 - self.c_bond.dy*10, y2_100 + self.c_bond.dx*10, x2_100 + self.c_bond.dy*10, y2_100 - self.c_bond.dx*10)

class Molecule(molecule.molecule):
    # initializes the Molecule
    def __str__(self):
        for i in range(self.atom_no):
            atom = Atom(self.get_atom(i))
            print(atom.__str__())

        for j in range(self.bond_no):
            bond = Bond(self.get_bond(j))
            print(bond.__str__())

    # returns a string that can be displayed as an svg file
    def svg(self):
        str = header
        atomcounter = 0
        bondcounter = 0
        # go through Atoms and Bonds until one list is done
        while(atomcounter < self.atom_no) and (bondcounter < self.bond_no):
            a1 = Atom(self.get_atom(atomcounter))
            b1 = Bond(self.get_bond(bondcounter))
            # find the Atom or Bond with the smallest z value
            # depending on which has the smallest z value, add that Atom or Bond to the svg string
            # then increase the counter of Atoms and Bonds found and set the temp variable to the next Atom or Bond
            if (a1.z < b1.z):
                str = str + a1.svg()
                atomcounter = atomcounter + 1
                
            else:
                str = str + b1.svg()
                bondcounter = bondcounter + 1

        # if not all Atoms have been added to the svg string, keep going through until they are all there
        while atomcounter < self.atom_no:
            str = str + a1.svg()
            atomcounter = atomcounter + 1  
            a1 = Atom(self.get_atom(atomcounter))
        
        # if not all Bonds have been added to the svg string, keep going through until thet are all there
        while bondcounter < self.bond_no:
            str = str + b1.svg()
            bondcounter = bondcounter + 1
            b1 = Bond(self.get_bond(bondcounter))

        str = str + footer
        return str

    def parse(self, file):
        # decode the bytes to be a string
        mol_str = file.decode()
        # split the file by lines
        list = mol_str.split("\n")
        # get the header as a string
        header = list[3].split()
        #find the number of Atoms and Bonds
        atommax = header[0]
        bondmax = header[1]
        # go through all the lines of atoms
        for i in range(int(atommax)):
            # get the current Atom line
            line = list[i+4].split() # +4 to skip the first few lines (they aren't atom lines)
            # append a new atom to the molecule based off the values on the line
            self.append_atom(line[3], float(line[0]), float(line[1]), float(line[2]))

        # go through all the lines for Bonds
        for i in range(int(bondmax)):
            # get the current Bond line
            line = list[i+4+int(atommax)].split() # +4 to skip the first few lines and then + atommax to skip all the atom lines
            # append a new bond to the molecule based off the values on the line
            self.append_bond(int(line[0])-1, int(line[1])-1, int(line[2]))
