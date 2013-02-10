#coding=utf-8
import numpy
import codecs
# @TODO 
# Numpy
# Heuristical search for the delimiter characters

class CsvIO:
    """Read and Write from/to a CSV-file
    It automatically infer the format of the given file and converts it to a numpy-array.
    Write to the file in the given format.
    """
    _delimiter=','
    _newline='\n'
    _fname=''
    _possible_delimiters=[',',';','\t','|','^']
    _possible_quotes=['"','\'','~']
    _handle=None
    def __init__(self,fname,delimiter=None,newline=None,quotedStrings=None,possible_delimiters=None,possible_quotes=None):
        """Initialize the CSV-File 
        Search for the delimiter and newline characters.
        Also find out which is the quotation Character, if there is any

        Keyword arguments:
        fname -- The filename
        delimiter -- optional delimiter
        newline -- optional newline character(s)
        quotedStrings -- empty, if the strings are not quoted, else the quotation character
        possible_delimiters -- Array of possible delimiter characters
        possible_quotes -- Array of possible quote characters
        """

        self._fname=fname

        #Set the possible characters
        if possible_delimiters!=None:
            self._possible_delimiters=possible_delimiters
        if possible_quotes!=None:
            self._possible_quotes=possible_quotes

        self._handle=codecs.open(fname,'r', "utf-8-sig") # automatic recognition of the encoding?

        line=self._handle.readline()
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

        self._handle.seek(0)

    def getConfig(self):
        """Get a dictionary with the configs for the CSV file"""
        return {
                'delimiter':self._delimiter,
                'newline':self._newline,
                'quotedStrings':self._quotedStrings
                }

    def setConfig(self,delimiter=None,newline=None,quotedStrings=None):
        """Set the config for the CSV file"""
        if delimiter!=None:
            self._delimiter=delimiter
        if newline!=None:
            self._newline=newline
        if quotedStrings!=None:
            self.quotedStrings=quotedStrings


    def readline(self):
        """Read and Parse a line of the CSV file
        return an 1D (numpy) Array of the data
        raise EOFError
        """
        line=self._handle.readline()
        if line=='':
            raise EOFError
        cols=line.split(self._delimiter)
        numpy_col=[]
        # Here we need the iter!
        i=iter(cols)
        while True:
            try:
                col=i.next()
            except StopIteration:
                break
            if col.rstrip()=='':
                numpy_col.append('')
                continue
            is_string=False # Do we need this?
            
            if self._quotedStrings!='':
                # When the string is quoted, everything is ok
                if col[0]==col.rstrip()[-1]==self._quotedStrings:
                    if col[-1]==self._newline:
                        col=col.rstrip()
                    col=col[1:-1]
                    is_string=True
                # If the string has only on the first position a quotation, 
                # than the string is not complete. We have to concatenate 
                # the current column with the next.
                elif col[0]==self._quotedStrings:
                    while col[-1]!=self._quotedStrings:
                        try:
                            nextcol=i.next()
                            col+=self._delimiter + nextcol
                        except StopIteration:
                            # The string continues on the next line
                            nline=self._handle.readline()
                            if nline=='': # O_o
                                raise EOFError
                            ncols=nline.split(self._delimiter)
                            cols.extend(ncols)
                            i=iter(ncols)
                            ncol=i.next()
                            col+=ncol
                    col=col[1:-1]
                    is_string=True
                # The column is not a string
                else:
                    is_string=False

            # numpy_col.append(numpy.fromstring(col))
            # @TODO Something like this...
            numpy_col.append(col)
        return numpy_col
    

    
    def read(self,names=True):
        """Return a 2-dimensional numpy-Array with the content of the CSV-file

        Keyword arguments:
        names -- Should the names be extracted from the first line of the CSV-file and saved in the dtype?
        """
        out=[]
        while True:
            try:
                out.append(self.readline())
            except EOFError:
                break
        return out

    def write(self,data,namesFromArray=True,fname=None):
        """Write a numpy-array to a CSV-file

        Keyword arguments:
        namesFromArray -- Should the names be extracted from the array and be written in the first line of the CSV-file?
        """
        write=''
        for row in data:
            i=0
            for col in row:
                if (isinstance(col,str) or isinstance(col,unicode)) and self._quotedStrings!='': # || numpy.dtype.???
                    col=self._quotedStrings + col + self._quotedStrings
                if i!=0: write+=self._delimiter
                write+=col
                i+=1
            write+=self._newline
        if fname==None:
            fname=self._fname
        with codecs.open(fname,'w','utf-8-sig') as handle:
            handle.write(write)
