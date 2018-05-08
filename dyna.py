import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import savgol_filter



def readcsv( filepath ):
    ''' Read the csv file and return a dictionnary
        the csv is in the format from the app PhysicsToolbox 
    '''
    
    rawdata = []
    with open(filepath, 'r') as file:  
        line = file.readline()
        
        while line:
            line = line.split(';')
            line = [ v.strip() for v in line ]
            line = [ v.replace(',', '.') for v in line ]
            line = [ v for v in line if v  ]
            if line:
                rawdata.append( line )

            line = file.readline()

    header = rawdata.pop(0)
    columns = list( zip( *rawdata ) )
    
    def convert( col ):
        col = [ float(v) for v in col ]
        col = np.array( col )
        return col
    
    data = { key:convert(values) for key, values in zip(header, columns) }
    
    return data


class Measure(  ):
    
    def __init__(self, data):
        ''' Create a Measure object
        
            - data is a dict
        '''
        self.data = data
        
        self.time = data['time']
        
        self.gFx = data['gFx']
        self.gFy = data['gFy']
        self.gFz = data['gFz']
        
        
    def setmask( self, dtStart, dtEnd ):
        
        time = self.data['time']
        mask = (time > dtStart)&(time < time[-1]-dtEnd)
        
        self.time = self.data['time'][mask]
        self.gFx = self.data['gFx'][mask]
        self.gFy = self.data['gFy'][mask]
        self.gFz = self.data['gFz'][mask]
        
        
    def smooth( self, window_length_sec ):
        dt = np.diff(self.time).mean()
        
        window_length_int = int( window_length_sec/dt/2 )*2 + 1 # have to odd
        polyorder = 2
        
        smoothit = lambda x: savgol_filter(x, window_length_int, polyorder, mode='nearest')
        
        self.gFx = smoothit( self.gFx )
        self.gFy = smoothit( self.gFy )
        self.gFz = smoothit( self.gFz )
        
        
    def plotGforces( self ):
        t_range = (min(self.time), max(self.time))
        
        gFx = self.gFx
        gFy = self.gFy
        gFz = self.gFz
        
        plt.figure(figsize=(12, 6))
        plt.subplot( 4, 1, 1 )
        plt.plot( self.time, gFx, '-' )
        plt.ylabel('gFx');
        plt.xlim( t_range )
        plt.tick_params(labelbottom='off')

        plt.subplot( 4, 1, 2 )
        plt.plot( self.time, gFy, '-' )
        plt.ylabel('gFy');
        plt.xlim( t_range )
        plt.tick_params(labelbottom='off')

        plt.subplot( 4, 1, 3 )
        plt.plot( self.time, gFz, '-' )
        plt.xlim( t_range )
        plt.ylabel('gFz');
        plt.tick_params(labelbottom='off')

        gFnorm = np.sqrt( gFx**2 + gFy**2 + gFz**2  )

        plt.subplot( 4, 1, 4 )
        plt.axhline( y=1, color='k', linewidth=1 )
        plt.plot( self.time, gFnorm, 'r-' )
        plt.xlabel('time (s)');
        plt.xlim( t_range )
        plt.ylabel('norm');