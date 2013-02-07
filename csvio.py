#!/usr/bin/python2.7
#coding=utf-8
import numpy
class CSVIO(object):
    _delimiter=','
    _newline='\n'
    def __init__(self,fname):
        """Initialize the CSV file
        @TODO The delimiters should be extracted automatically from the file
        """
        self.fname=fname
    def read(self,names=True):
        """Return a 2-dimensional numpy-Array with the content of the CSV-file

        Keyword arguments:
        names -- Should the names be extracted from the first line of the CSV-file and saved in the dtype?
        """
        return numpy.genfromtxt(self.fname,delimiter=self._delimiter,names=names,dtype=None,invalid_raise=False)
    def write(self,fname,data,names=True):
        """Write a numpy-array to a CSV-file

        Keyword arguments:
        fname -- filename
        data -- The numpy-array
        names -- Should the names be extracted from the array and be written in the first line of the CSV-file?
        """
        write=[]
        if names==True:
            names=[]
            for tup in data.dtype.descr:
                names.append(tup[0])
            write.append(self._delimiter.join(names))
        for row in data:
            write.append(self._delimiter.join(map(str,row)))
        handle=file(fname,'w')
        for r in write:
            handle.write(r+self._newline)
        handle.close()
