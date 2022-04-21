#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#
"""
    @package
    Generate a csv BOM list.
    Components are sorted by ref and grouped by value
    Fields are (if exist)
    Item, Qty, Reference(s), Value, LibPart, Footprint, Datasheet

    Command line:
    python "pathToFile/bom_csv_grouped_by_value.py" "%I" "%O.csv"
"""


from __future__ import print_function

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

def myEqu(self, other):
    """myEqu is a more advanced equivalence function for components which is
    used by component grouping. Normal operation is to group components based
    on their value and footprint.

    In this example of a custom equivalency operator we compare the
    value, the part name and the footprint.
    """
    result = True
    if self.getValue() != other.getValue():
        result = False
    elif self.getField("MPN") != other.getField("MPN"):
        result = False
    elif self.getField("Manufacturer") != other.getField("Manufacturer"):
        result = False
    elif self.getField("DNP") != other.getField("DNP"):
        result = False

    return result

# Override the component equivalence operator - it is important to do this
# before loading the netlist, otherwise all components will have the original
# equivalency operator.
kicad_netlist_reader.comp.__eq__ = myEqu

if len(sys.argv) != 3:
    print("Usage ", __file__, "<generic_netlist.xml> <output.csv>", file=sys.stderr)
    sys.exit(1)


# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

# subset the components to those wanted in the BOM, controlled
# by <configure> block in kicad_netlist_reader.py
components = net.getInterestingComponents()

# prepend an initial 'hard coded' list and put the enchillada into list 'columns'
# this is where the collumns you want extracted from each part is defined, make sure the string matched exactly the field in the the components.
# You also need to add the collumn to the row append statements below
columns = ['Designator', 'Qty', 'DNP', 'Value', 'Description', 'Manufacturer', 'MPN', 'Footprint', 'SMT/THT', 'SOURCE', 'SRCPN', 'Alternate Manufacturer 1', 'Alternate MPN 1', 'Alternate Manufacturer 2', 'Alternate MPN 2'] 

# Create a new csv writer object to use as the output formatter
out = csv.writer( f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL )

# override csv.writer's writerow() to support encoding conversion (initial encoding is utf8):
def writerow( acsvwriter, columns ):
    utf8row = []
    for col in columns:
        utf8row.append( str(col) )  # currently, no change
    acsvwriter.writerow( utf8row )

# Output a set of rows as a header providing general information
writerow( out, ['Source:', net.getSource()] )
writerow( out, ['Date:', net.getDate()] )
writerow( out, ['Tool:', net.getTool()] )
writerow( out, ['Generator:', sys.argv[0]] )
writerow( out, ['Component Count:', len(components)] )
writerow( out, [] )

row = []

writerow( out, ['Collated Components:'] )
writerow( out, [] )                        # blank line
writerow( out, columns )                   # reuse same columns

# Get all of the components in groups of matching parts + values
# (see kicad_netlist_reader.py)
grouped = net.groupComponents(components)


# Output component information organized by group, aka as collated:
for group in grouped:
    del row[:]
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        if len(refs) > 0:
            refs += ", "
        refs += component.getRef()
        c = component

    # Fill in the component groups common data
    row.append( refs )
    row.append( len(group) )
    row.append( net.getGroupField(group, columns[2]) ) #DNP
    row.append( c.getValue() )
    row.append( net.getGroupField(group, columns[4]) ) #Description
    row.append( net.getGroupField(group, columns[5]) ) #Manufacturer
    row.append( net.getGroupField(group, columns[6]) ) #MPN
    row.append( net.getGroupFootprint(group) )
    row.append( net.getGroupField(group, columns[8]) ) #SMT/THT
    row.append( net.getGroupField(group, columns[9]) ) #SOURCE
    row.append( net.getGroupField(group, columns[10]) ) #SRCPN
    row.append( net.getGroupField(group, columns[11]) ) #Alternate Manufacturer 1
    row.append( net.getGroupField(group, columns[12]) ) #Alternate MPN 1
    row.append( net.getGroupField(group, columns[13]) ) #Alternate Manufacturer 2
    row.append( net.getGroupField(group, columns[14]) ) #Alternate MPN 2

    writerow( out, row  )


f.close()
