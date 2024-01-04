#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "mol.h"

//Sets the values of an atom
void atomset( atom *atom, char element[3], double *x, double *y, double *z )
{
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}

//Sets the values of variables to be the same as their counterparts in the atom
void atomget( atom *atom, char element[3], double *x, double *y, double *z )
{
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
    strcpy(element, atom->element);
}

//Sets the values of a bond
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs )
{
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

//Sets the values of variables to be the same as their counterparts in the bond
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs )
{
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

//Sets the coordinate values in the bond based off of the positioning of the two atoms in the bond
void compute_coords( bond *bond )
{
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;
    double xVal = bond->atoms[bond->a2].x - bond->atoms[bond->a1].x;
    double yVal = bond->atoms[bond->a2].y - bond->atoms[bond->a1].y;
    bond->len = sqrt(xVal * xVal + yVal * yVal);
    bond->dx = (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) / bond->len;
    bond->dy = (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) / bond->len;
}

//Create enough space for a molecule
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max )
{
    molecule *mol = malloc(sizeof(molecule));
    if (mol == NULL)
    {
        return NULL; //If any call to malloc() fails, the function will return NULL.
    } //This if statement is done for all calls to malloc()
    mol->atom_max = atom_max;
    mol->atom_no = 0; //Molecule starts with no atoms
    mol->atoms = malloc(sizeof(atom) * atom_max);
    if (mol->atoms == NULL)
    {
        return NULL;
    }
    mol->atom_ptrs = malloc(sizeof(atom*) * atom_max);
    if (mol->atom_ptrs == NULL)
    {
        return NULL;
    }
    mol->bond_max = bond_max;
    mol->bond_no = 0; //Molecule starts with no bonds
    mol->bonds = malloc(sizeof(bond) * bond_max);
    if (mol->bonds == NULL)
    {
        return NULL;
    }
    mol->bond_ptrs = malloc(sizeof(bond*) * bond_max);
    if (mol->bond_ptrs == NULL)
    {
        return NULL;
    }

    return mol;
}

//Creates a copy of a molecule
molecule *molcopy( molecule *src )
{
    molecule *mol = molmalloc(src->atom_max, src->bond_max);
    if (mol == NULL)
    {
        return NULL;
    }
    mol->atom_max = src->atom_max;
    mol->bond_max = src->bond_max;
    mol->atom_no = 0; //The atom and bond numbers starts at 0 instead of the numbers in the original molecule. This is because appending atoms and bonds raises the number already 
    mol->bond_no = 0; //If the values were set to be equal to the last molecule, the final value would be double what it should be
    for (int i = 0 ; i < src->atom_no; i++)
    {
        molappend_atom(mol, &src->atoms[i]);
    }
    for (int i = 0 ; i < src->bond_no; i++)
    {
        molappend_bond(mol, &src->bonds[i]);
    }

    return mol;
}

//Frees a molecule
void molfree( molecule *ptr )
{
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

//Adds an atom to a molecule
void molappend_atom( molecule *molecule, atom *atom )
{
    if(molecule->atom_no == molecule->atom_max) //Any resizing will only happen if the molecule is full (The number of atoms/bonds is equal to the max)
    {
        if (molecule->atom_max == 0) //Has to be separate case if the max is 0 as you can't change 0 by doubling it
        {
            molecule->atom_max = 1;
        }
        else
        {
            molecule->atom_max = molecule->atom_max * 2;
        }
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        if(molecule->atoms == NULL)
        {
            printf("Realloc failed. Exiting...\n"); //The molappend_atom function returns void so it is impossible to return NULL is the realloc fails
            exit(0); //Instead, the whole program will be terminated. This is also done below and in the molappend_bond function as well
        }
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));
        if(molecule->atom_ptrs == NULL)
        {
            printf("Realloc failed. Exiting...\n");
            exit(0);
        }
        for(int i = 0; i < molecule->atom_max; i++)
        {
            molecule->atom_ptrs[i] = &molecule->atoms[i]; //This loop points the pointer array to the atom array as the atom array may have moved froim the realloc
        }
    }

    memcpy(&molecule->atoms[molecule->atom_no], atom, sizeof(struct atom));
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    molecule->atom_no++;
}

//Adds a bond to a molecule
//Very similar to molappend_atom
void molappend_bond( molecule *molecule, bond *bond )
{
    if(molecule->bond_no == molecule->bond_max)
    {
        if (molecule->bond_max == 0)
        {
            molecule->bond_max = 1;
        }
        else
        {
            molecule->bond_max = molecule->bond_max * 2;
        }
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        if(molecule->bonds == NULL)
        {
            printf("Realloc failed. Exiting...\n");
            exit(0);
        }
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));
        if(molecule->bond_ptrs == NULL)
        {
            printf("Realloc failed. Exiting...\n");
            exit(0);
        }
        for(int i = 0; i < molecule->bond_max; i++)
        {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }

    bond->atoms = molecule->atoms;
    memcpy(&molecule->bonds[molecule->bond_no], bond, sizeof(struct bond));
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    molecule->bond_no++;
}

//Function that compares 2 atoms to be used for qsort()
int compare_atom (const void *xVoid, const void *yVoid)
{
    atom *xAtom = *(atom **)xVoid;
    atom *yAtom = *(atom **)yVoid;

    double result = xAtom->z - yAtom->z;
    
    //Used if and else if statements instead of a simple "return xAtom->z - yAtom->z;"
    //This is because the z values are doubles and the function returns an integer
    //Rare rounding case may cause errors and I didn't want to bother messing with that
    //For example: 1-0.75 = 0.25 but when converting a double to an int, that value could be rounded to 0 when really you want the value returned to be > 0
    if (result < 0)
    {
        return -1;
    }
    else if (result > 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

//Function that compares 2 bonds to be used for qsort()
//Very similar to the compare_atom function
int compare_bond (const void *xVoid, const void *yVoid)
{
    bond *xBond = *(bond **)xVoid;
    bond *yBond = *(bond **)yVoid;

    double result = xBond->z - yBond->z;
    
    //Same if and if else statements as last function
    if (result < 0)
    {
        return -1;
    }
    else if (result > 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

//Simple function to sort the molecule pointer array by using qsort()
void molsort( molecule *molecule )
{
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), compare_atom);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), compare_bond);
}

//Sets up the xform_matrix for an x-rotation
void xrotation( xform_matrix xform_matrix, unsigned short deg )
{
    double rad = deg * (M_PI / 180.0); //Converts degrees to radian
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

//Sets up the xform_matrix for a y-rotation
void yrotation( xform_matrix xform_matrix, unsigned short deg )
{
    double rad = deg * (M_PI / 180.0);
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

//Sets up the xform_matrix for a z-rotation
void zrotation( xform_matrix xform_matrix, unsigned short deg )
{
    double rad = deg * (M_PI / 180.0);
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

//Rotates all the atoms in the molecule by the values in the xform_matrix
void mol_xform( molecule *molecule, xform_matrix matrix )
{
    for (int i = 0; i < molecule->atom_no; i++) //Loop through all atoms
    {
        atom *atm = molecule->atoms + i; //Pointer to the current atom
        double x = matrix[0][0] * atm->x + matrix[0][1] * atm->y + matrix[0][2] * atm->z; //Get x, y and z values through matrix multiplication
        double y = matrix[1][0] * atm->x + matrix[1][1] * atm->y + matrix[1][2] * atm->z;
        double z = matrix[2][0] * atm->x + matrix[2][1] * atm->y + matrix[2][2] * atm->z;
        atm->x = x; //Set new values
        atm->y = y;
        atm->z = z;
    }

    //Compute the new coordinates of the bonds (since the coordinates of all the atoms changed)
    for (int i = 0; i < molecule->bond_no; i++)
    {
        bond *bnd = molecule->bonds + i;
        compute_coords(bnd);
    }
}
