import sqlite3
import os
import MolDisplay

class Database:
    # initializes the database
    def __init__(self, reset=False):
        if (reset == True):
            os.remove( 'molecules.db' )

        self.conn = sqlite3.connect( 'molecules.db' )
        self.cur = self.conn.cursor()
    
    # creates all the necessary tables
    def create_tables(self):
        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Elements' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE Elements
                 ( ELEMENT_NO   INTEGER NOT NULL,
                   ELEMENT_CODE VARCHAR(3) NOT NULL,
                   ELEMENT_NAME VARCHAR(32) NOT NULL,
                   COLOUR1      CHAR(6) NOT NULL,
                   COLOUR2      CHAR(6) NOT NULL,
                   COLOUR3      CHAR(6) NOT NULL,
                   RADIUS       DECIMAL(3) NOT NULL,
                   PRIMARY KEY (ELEMENT_CODE) );""" )

        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Atoms' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE Atoms
                 ( ATOM_ID      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   ELEMENT_CODE VARCHAR(3) NOT NULL,
                   X            DECIMAL(7 , 4) NOT NULL,
                   Y            DECIMAL(7 , 4) NOT NULL,
                   Z            DECIMAL(7 , 4) NOT NULL,
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""")

        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Bonds' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE Bonds
                 ( BOND_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   A1      INTEGER NOT NULL,
                   A2      INTEGER NOT NULL,
                   EPAIRS  INTEGER NOT NULL );""")
            
        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Molecules' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE Molecules
                 ( MOLECULE_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   NAME        TEXT NOT NULL UNIQUE,
                   ATOM_NO     INTEGER NOT NULL,
                   BOND_NO     INTEGER NOT NULL );""")

        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MoleculeAtom' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE MoleculeAtom
                 ( MOLECULE_ID INTEGER NOT NULL,
                   ATOM_ID     INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID,ATOM_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""")
            
        if(self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MoleculeBond' ''').fetchone()[0] == 0):
            self.cur.execute( """CREATE TABLE MoleculeBond
                 ( MOLECULE_ID INTEGER NOT NULL,
                   BOND_ID     INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID,BOND_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (BOND_ID) REFERENCES Bonds );""")
    
    # adds a row to a table depending on which table is specified
    def __setitem__(self, table, values):
        if(table == "Elements"):
            data = [(values[0], values[1], values[2], values[3], values[4], values[5], values[6])]
            self.cur.executemany("INSERT INTO " + table + " VALUES(?, ? ,? ,?, ?, ?, ?)", data)
            self.conn.commit()
        
        if(table == "Atoms"):
            data = [(values[0], values[1], values[2], values[3])]
            self.cur.executemany("INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) VALUES(?, ?, ?, ?)", data)
        
        if(table == "Bonds"):
            data = [(values[0], values[1], values[2])]
            self.cur.executemany("INSERT INTO Bonds(A1, A2, EPAIRS) VALUES(?, ?, ?)", data)
        
        if(table == "Molecules"):
            data = [(values[0], values[1], values[2])]
            self.cur.executemany("INSERT INTO Molecules(NAME, ATOM_NO, BOND_NO) VALUES(?, ?, ?)", data)

        if(table == "MoleculeAtom"):
            data = [(values[0], values[1])]
            self.cur.executemany("INSERT INTO MoleculeAtom(MOLECULE_ID, ATOM_ID) VALUES (?, ?)", data)

        if(table == "MoleculeBond"):
            data = [(values[0], values[1])]
            self.cur.executemany("INSERT INTO MoleculeBond(MOLECULE_ID, BOND_ID) VALUES (?, ?)", data)

    # adds an atom to the Atoms table and adds the atom id and the molecule id to the MoleculeAtom table
    def add_atom(self, molname, atom):

        self['Atoms'] = (atom.c_atom.element, atom.c_atom.x, atom.c_atom.y, atom.c_atom.z)

        mol_id = self.cur.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?", (molname,)).fetchone() # get the molecule id
        atom_id = self.cur.lastrowid # get the last atom id inserted

        self['MoleculeAtom'] = (mol_id[0], atom_id)

    # adds an bond to the Bonds table and adds the bond id and the molecule id to the MoleculeBond table
    def add_bond(self, molname, bond):
        
        self['Bonds'] = (bond.c_bond.a1, bond.c_bond.a2, bond.c_bond.epairs)

        mol_id = self.cur.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?", (molname,)).fetchone() # get the molecule id
        bond_id = self.cur.lastrowid # get the last bond id inserted

        self['MoleculeBond'] = (mol_id[0], bond_id)

    # adds a new molecule to the Molecules table based off the svg file provided and then calls add_atom and add_bond for each atom and bond in the molecule
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        self['Molecules'] = (name, mol.atom_no, mol.bond_no)

        for i in range(mol.atom_no):
            atom = MolDisplay.Atom(mol.get_atom(i))
            self.add_atom(name, atom)

        for i in range(mol.bond_no):
            bond = MolDisplay.Bond(mol.get_bond(i))
            self.add_bond(name, bond)

        self.conn.commit()

    # loads a molecule from the database (specified by name) by storing all the atoms and bonds into a new molecule
    # returns that new molecule
    def load_mol(self, name):
        mol = MolDisplay.Molecule()

        query = """SELECT ELEMENT_CODE, X, Y, Z
                   FROM Atoms
                   JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                   JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                   WHERE Molecules.NAME = ?
                   ORDER BY Atoms.ATOM_ID"""
        self.cur.execute(query, (name,))
        atoms = self.cur.fetchall()
        
        for atom in atoms:
            mol.append_atom(atom[0], atom[1], atom[2], atom[3])

        query = """SELECT A1, A2, EPAIRS
                   FROM Bonds
                   JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID
                   JOIN Molecules ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                   WHERE Molecules.NAME = ?
                   ORDER BY Bonds.BOND_ID"""
        self.cur.execute(query, (name,))
        bonds = self.cur.fetchall()

        for bond in bonds:
            mol.append_bond(bond[0], bond[1], bond[2])

        return mol
    
    # creates a dictionary for the radii of the elements in the Elements table and returns it
    def radius(self):
        self.cur.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements")
        elements = self.cur.fetchall()

        radii = {}
        # for each element, set an item in the dictionary
        for element in elements:
            radii[element[0]] = element[1]

        return radii
    
    # creates a dictionary for the names of the elements in the Elements table and returns it
    def element_name(self):
        self.cur.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements")
        elements = self.cur.fetchall()

        element_names = {}
        # for each element, set an item in the dictionary
        for element in elements:
            element_names[element[0]] = element[1]

        return element_names
    
    # adds a gradient definition to a string for each element in the Elements table and then returns that string to add to an svg file
    def radial_gradients(self):
        self.cur.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")
        gradients = self.cur.fetchall()

        total_gradients = ""
        for gradient in gradients:
            radialGradientSVG = """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
    <stop offset="0%%" stop-color="#%s"/>
    <stop offset="50%%" stop-color="#%s"/>
    <stop offset="100%%" stop-color="#%s"/>
</radialGradient>""" % (gradient[0], gradient[1], gradient[2], gradient[3])

            total_gradients += radialGradientSVG # add the gradient to the total string
        radialGradientSVG = """<radialGradient id="default" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
    <stop offset="0%%" stop-color="#000000"/>
    <stop offset="50%%" stop-color="#000000"/>
    <stop offset="100%%" stop-color="#000000"/>
</radialGradient>"""
        total_gradients += radialGradientSVG # add the gradient to the total string

        return total_gradients

if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    fp = open( 'water-3D-structure-CT1000292221.sdf' );
    db.add_molecule( 'Water', fp );
    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    db.add_molecule( 'Caffeine', fp );
    fp = open( 'CID_31260.sdf' );
    db.add_molecule( 'Isopentanol', fp );
    # display tables
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );

    MolDisplay.radius = db.radius();
    MolDisplay.element_name = db.element_name();
    MolDisplay.header += db.radial_gradients();
    for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
        mol = db.load_mol( molecule );
        mol.sort();
        fp = open( molecule + ".svg", "w" );
        fp.write( mol.svg() );
        fp.close();