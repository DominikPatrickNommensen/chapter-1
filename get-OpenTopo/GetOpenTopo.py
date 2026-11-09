import os
import requests

class GetOpenTopo:
    """ 
    This class downloads a GeoTiff from OpenTopography of a region 
    of interest in a public global topography dataset.
    
    Attributes
    ----------
    bounds : tuple
        The bounding values for a rectangle where topography data.
        Format is south, north, west, east.
    output_directory : str
        The directory where the GeoTiff should be saved (default value 
        is the current directory).
    demtype : str
        The global dataset used. Options are 'SRTMGL3', 'SRTMGL1', 
        'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 
        'COP30', 'COP90' (default value is 'AW3D30').
    api_key : str
        The user API key for OpenTopography which can be found in the
        MyOpenTopo portal (default: 'demoapikeyot2022').
        
    Methods
    -------
    download_topography()
        Downloads topography data based on the specified parameters.
    get_api_url()
        Returns the constructed API URL for OpenTopography.
    get_bounds()
        Returns the specified bounding values.
    """

    def __init__(self, bounds, output_directory='./', demtype='AW3D30', api_key='demoapikeyot2022'):
        """
        Initialize the GetOpenTopo instance.

        Parameters
        ----------
        bounds : tuple
            The bounding values for a rectangle where topography data.
            Format is south, north, west, east.
        output_directory : str, optional
            The directory where the GeoTiff should be saved (default value 
            is the current directory).
        demtype : str, optional
            The global dataset used. Options are 'SRTMGL3', 'SRTMGL1', 
            'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 
            'COP30', 'COP90' (default value is 'AW3D30').
        api_key : str, optional
            The user API key for OpenTopography which can be found in the
            MyOpenTopo portal (default: 'demoapikeyot2022').
        """

        self.__bounds = bounds
        south, north, west, east = self.__bounds
        
        self._validate_bounds(south, north, west, east)
        self._validate_demtype(demtype)
        self._validate_path(output_directory)
        
        self.__output_directory = output_directory
        self.__filename = self._create_filename(demtype, south, north, west, east)
        self.__api_url = self._create_api_url(demtype, south, north, west, east, api_key)
    
    def _validate_bounds(self, south, north, west, east):
        """Validate the bounds."""
        if west >= east:
            raise ValueError('west bound must be less than east bound')
        if south >= north:
            raise ValueError('south bound must be less than north bound')
    
    def _validate_demtype(self, demtype):
        """Validate the demtype."""
        demtypes = ['SRTMGL3', 'SRTMGL1', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 
                    'SRTM15Plus', 'NASADEM', 'COP30', 'COP90']
        
        if demtype not in demtypes:
            raise ValueError('demtype must be one of the following:\n' + '\n'.join(demtypes))
    
    def _validate_path(self, directory):
        """Validate the output directory path."""
        if not os.path.isdir(directory):
            raise ValueError('directory must exist')
    
    def _create_filename(self, demtype, south, north, west, east):
        """Create the filename for the GeoTiff."""
        return 'OpenTopo_{}_S{}_N{}_W{}_E{}.tif'.format(demtype, south, north, west, east)
    
    def _create_api_url(self, demtype, south, north, west, east, api_key):
        """Create the API URL for OpenTopography."""
        base_api_url = 'https://portal.opentopography.org/API/globaldem?'
        requested_tile = ('demtype={}&south={}&north={}&west={}&east={}' +
                         '&outputFormat=GTiff&API_Key={}')
        return base_api_url + requested_tile.format(demtype, south, north, west, east, api_key)
    
    def download_topography(self):
        """Download topography data."""
        r = requests.get(self.__api_url, stream=True)
        if r.status_code == 200:
            with open(os.path.join(self.__output_directory, self.__filename), 'wb') as f:
                f.write(r.content)
            print('Topography successfully downloaded.')
        elif r.status_code == 400:
            return 'Bad request to OpenTopography. Could be due to size; try decreasing bounds.'
        elif r.status_code == 401:
            return 'Unauthorized access to OpenTopography. Could be API Key.'
        elif r.status_code == 500:
            return 'Internal Error with OpenTopography.'
        return os.path.join(self.__output_directory, self.__filename)
    
    def get_api_url(self):
        """Get the constructed API URL."""
        return self.__api_url
    
    def get_bounds(self):
        """Get the specified bounding values."""
        return self.__bounds

    def get_filename(self):
        """Get the filename for the GeoTiff."""
        return self.__filename

if __name__=='__main__':
    print('This is a class to get Topography from OpenTopography. You should import the class into your project, not executing this file.')