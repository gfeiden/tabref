# tabref.py

Numerically order table reference with ease.

## Purpose
The purpose of the routines listed below is to extract and 
sequentially number, in order of appearance, citations from a LaTeX 
table that uses the deluxetable environment from AASTeX.
          
## Dependencies
Functions contained below rely only on the standard Python libraries
'sys' and 'fileinput'.
                      
## Notes
The file input into the module must contain a LaTeX table formatted 
using the deluxetable environment from the AASTeX or emulateapj 
packages.
    
## Examples
Before demonstrating how to call the script, you'll want to know what
you'll need for input and what to expect as output.

### Input
 * f : String of the file name containing a LaTeX table.

 * cols : (Optional) List or tuple whose elements are the column number
          for the citation columns.

### Output
 * f_new : Reconstructed LaTeX file containing updated table with the
           file name: <filename>.tex_new

The function may be called from the command line:

```shell    
python tabref.py ./dir/<filename>.tex col1 col2 ...
```       
                 
Alternatively, the function may be called from within a python shell:

```python    
import tabref
tabref.order_refs('./dir/<filename>' [, cols=(col1,col2)])
```

where the 'cols' argument is optional only if the last column in the 
table contains citations.
                
