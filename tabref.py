"""
    Beer-Ware Licence (Revision 42)
    -------------------------------
    Gregory A. Feiden wrote this file. As long as you retain this notice 
    you can do whatever you want with this stuff. If we meet some day and 
    you think this stuff is worth it, you can buy me a beer in return.
    
    Purpose
    -------
    The purpose of the routines listed below is to extract and 
    sequentially number, in order of appearance, citations from a LaTeX 
    table that uses the deluxetable environment from AASTeX.
          
    Input
    -----
    f : String of the file name containing a LaTeX table.
    
    cols : (Optional) List or tuple whose elements are the column number 
           for the citation columns.
   
    Output
    ------
    f_new : Reconstructed LaTeX file containing updated table with the
            file name: <filename>.tex_new
            
    Dependencies
    ------------
    Functions contained below rely only on the standard Python libraries
    'sys' and 'fileinput'.
                      
    Notes
    ------
    The file input into the module must contain a LaTeX table formatted 
    using the deluxetable environment from the AASTeX or emulateapj 
    packages.
    
    Examples
    --------
    The function may be called from the command line:
    
                $ python tabref.py ./dir/<filename>.tex col1 col2 ...
                        
    Alternatively, the function may be called from within a python shell:
    
                >>> import tabref
                >>> tabref.order_refs('./dir/<filename>' [, cols=(col1,col2)])
    
    where the 'cols' argument is optional only if the last column in the 
    table contains citations.
                
    Author
    ------
    Gregory A. Feiden  <gregory.a.feiden.gr@dartmouth.edu>
    
    Date
    ----
    12 Nov 2012
  
"""
__all__ = [ 'check_files', 'create_ref_dict', 'order_refs', 'tablenotegen',
            'write_to_file' ]
            
import sys
import fileinput as _fi

table_refs = {}    # initialize empty dictionary for table references


def check_file(f):
    """ 
    Checks to confirm that all required files are present. 
    
    Parameters
    ----------
    f : Name of a file containing a LaTeX table. No file extension is 
        required as the function automatically prescribes the necessary
        extension.
    
    """  
    try:
        open(f, 'r')
    except IOError:
        sys.exit('\nWhoops! LaTeX document {0} does not exist.\n'.format(f))
                  

def create_ref_dict(refs):
    """ 
    Create a dictionary that contains all references cited in the table.
    
    All references mentioned in the table will be assigned an integer 
    number according to their order of appearance within the table. The
    order of appearance is determined by the LaTeX compiler and is not 
    determined here.
    
    Parameters
    ----------
    ref : List containing all of the references extracted from the table.
    
    Output
    ------
    table_refs : An initially blank global dictionary to which items, in
                 this case reference/integer pairs, are added.
                 
    """
    i = 1
    for line in refs:
        for col in line:
            for item in col:
                if table_refs.has_key(item):
                    pass
                else:
                    table_refs[item] = i 
                    i += 1


def table_note_gen(refs):
    """ 
    Generate ordered reference list as a string.
    
    The references appearing in the LaTeX table are sorted by order of
    appearance and are then parsed into a single string in the form of
    the \tablenotetext LaTeX environment.
    
    Parameters
    ----------
    refs : List containing all references cited in the LaTeX table.
    
    Returns
    -------
    notes : String containing the references, properly ordered, in the
            \tablenotetext environment.
    
    """
    src = sorted(table_refs.items(), key=lambda x: x[1])

    clist = ''.join(['(%s) \\citet{%s}, ' % (str(x[1]), x[0]) for x in src]) 
       
    note = '\\tablenotetext{}{{\\bf References.} ' + clist.rstrip(', ') + '}'
    
    return note
        

def order_refs(f, cols='Last'):
    """ 
    Order table references in a latex table.
    
    Parameters
    ----------
    f : Name of the file containing the LaTeX table. An extension may be
        included, but the actual name of the file (as a string) is all 
        that is required.
    
    cols : (Optional) Tuple or list with the elements of the tuple being 
           the column numbers that contain citations.
        
    Output
    ------
    f_new : Name of new file that contains the reconstructed LaTeX table
            with in table citations replaced with the reference number 
            and containing the \tablenotetext string. File name will be
            the same as the old, but with the extension '.tex_new'.
    
    Example
    -------
    Say you want to order the references in a table contained in the 
    file ./test/table.tex. The function can then be called by
                     
                >>> import tabref
                >>> tabref.order_refs('./test/table.tex', cols=(3, 6))
                
    """
    check_file(f)
    
    table = [x for x in _fi.input(f)]
    _fi.close()
        
    start = table.index('\\startdata\n')
    end = table.index('\\enddata\n')
    
    data = [x.rstrip('\n').rstrip().rstrip('\\\\').split('&') 
            for x in table[start + 1 : end]]
    
    if cols == 'Last':
        col = [len(data[0]) - 1]
    else:
        col = [x for x in cols]
    
    cites = [[x[c][x[c].index('{') + 1 : x[c].index('}')] for c in col]
           for x in data]
    
    refs = [[x[i].split(',') for i in range(len(col))] for x in cites]
               
    create_ref_dict(refs)
    
    tablenote = table_note_gen(refs)
        
    for i in range(len(data)):
        
        for j in range(len(col)):
            c = col[j]
            
            for r in refs[i][j]:
                data[i][c] = data[i][c].replace(r, str(table_refs[r]))
            
            data[i][c] = data[i][c].replace('\\citet{', '').replace('\\citep{', '')
            data[i][c] = data[i][c].replace('\\cite{', '').replace('}', '')
             
            data[i][c] = ', '.join(sorted(data[i][c].rstrip().lstrip().split(',')))
            
    data_new = [' & '.join(line) for line in data]
        
    write_to_file(f, table, data_new, tablenote, start, end)


def write_to_file(f, table, data, tablenote, start, end):    
    """ write results to file """
    fout = open(f + '_new', 'w')
    
    for i in range(start + 1):
        fout.write(table[i])
    
    for i in range(len(data)):
        x = data[i]
        if i < len(data) - 1:
            x += ' \\\\'
        else:
            pass
        fout.write(x + '\n')
    
    fout.write(table[end] + '\n')    
    fout.write(tablenote + '\n')
    
    for i in range(end + 1, len(table)):
        fout.write(table[i])
    
    fout.close()


if __name__ == '__main__':
    """ Port a command line call to the routine as a function call. """ 
    n_args = len(sys.argv)
    
    if n_args < 2:
        order_refs(sys.argv[1])
    else:
        columns = [float(sys.argv[i]) for i in n_args if i > 1]
        order_refs(sys.argv[1], cols=columns)
