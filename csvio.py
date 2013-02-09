#coding=utf-8
import numpy
class CsvIO:
    _delimiter=','
    _newline='\n'
    _fname=''
    _possible_delimiters=[',',';','\t','|','^']
    _possible_quotes=['"','\'','~']
    def __init__(self,fname,delimiter=None,newline=None,quotedStrings=None,possible_delimiters=None,possible_quotes=None):
        """Initialize the CSV-File 
        Search for the delimiter and newline characters.
        Also find out which is the quotation Character, if there is any

        Keyword arguments:
        fname -- The filename
        delimiter -- optional delimiter (default: None)
        newline -- optional newline character(s) (default: None)
        quotedStrings -- empty, if the strings are not quoted, else the quotation character (default: None)
        possible_delimiters -- Array of possible delimiter characters
        possible_quotes -- Array of possible quote characters
        """

        #Set the possible characters
        if possible_delimiters!=None:
            self._possible_delimiters=possible_delimiters
        if possible_quotes!=None:
            self._possible_quotes=possible_quotes

        with file(fname,'r') as handle:
            line=handle.readline()
            # Find newline Character
            # Two last characters=\r\n -> Windows
            # Last Character=\n -> UNIX
            if newline==None:
                if line[-2:].strip()==line[-2:]:
                    self._newline=line[-2:]
                else:
                    self._newline=line[-1:]
            else:
                self._newline=newline

            # Find delimiter
            # idea: count the possible delimiters, the most common character could be the delimiter
            # is there any better idea?
            if delimiter==None:
                count_d=dict()
                for d in self._possible_delimiters:
                    count_d[d]=line.count(d)
                delimiter=max(count_d,key=count_d.get)
            self._delimiter=delimiter

            # Find out if strings are quoted
            if quotedStrings==None:
                splitted=line.split(self._delimiter,5)
                count_quotes=dict((k,0) for k in self._possible_quotes)
                for col in splitted:
                    for q in self._possible_quotes:
                        if col[0]==q==col[-1]:
                            count_quotes[q]+=1
                quotedStrings=max(count_quotes,key=count_quotes.get)
                if count_quotes[quotedStrings]==0:
                    quotedStrings=''
            self._quotedStrings=quotedStrings

    def getConfig(self):
        """Get a dictionary with the configs for the CSV file"""
        return {
                'delimiter':self._delimiter,
                'newline':self._newline,
                'quotedStrings':self._quotedStrings
                }
    def setConfig(self=None,delimiter=None,newline=None,quotedStrings=None):
        """Set the config for the CSV file"""
        if delimiter!=None:
            self._delimiter=delimiter
        if newline!=None:
            self._newline=newline
        if quotedStrings!=None:
            self.quotedStrings=quotedStrings


    
    def read(self,names=True):
        """Return a 2-dimensional numpy-Array with the content of the CSV-file

        Keyword arguments:
        names -- Should the names be extracted from the first line of the CSV-file and saved in the dtype?
        """
        return numpy.genfromtxt(fname,delimiter=_delimiter,names=names,dtype=None,invalid_raise=False)
    def write(self,data,namesFromArray=True):
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
