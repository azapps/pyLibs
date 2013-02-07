#coding=utf-8
import numpy
_delimiter=','
_newline='\n'
def read(fname,names=True):
    """Return a 2-dimensional numpy-Array with the content of the CSV-file

    Keyword arguments:
    names -- Should the names be extracted from the first line of the CSV-file and saved in the dtype?
    """
    return numpy.genfromtxt(fname,delimiter=_delimiter,names=names,dtype=None,invalid_raise=False)
def write(fname,data,namesFromArray=True):
    """Write a numpy-array to a CSV-file

    Keyword arguments:
    fname -- filename
    data -- The numpy-array
    namesFromArray -- Should the names be extracted from the array and be written in the first line of the CSV-file?
    """
    write=[]
    if namesFromArray==True:
        names=[]
        for tup in data.dtype.descr:
            names.append(tup[0])
        write.append(_delimiter.join(names))
    for row in data:
        write.append(_delimiter.join(map(str,row)))
    with file(fname,'w') as handle:
        for r in write:
            handle.write(r+_newline)
