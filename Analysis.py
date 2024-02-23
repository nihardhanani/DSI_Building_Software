import matplotlib.pyplot as plt
import yaml
import requests
import logging
import subprocess
import statistics
import pandas as pd

class Analysis():
    config_path = ['configuration/system_config.yml', 'configuration/user_config.yml']

    def __init__(self, analysis_config: str) -> None:
        config = {}
        config_path = ['configuration/system_config.yml', 'configuration/user_config.yml']

        # load each config file and update the config dictionary
        for path in config_path :
            with open(path, 'r') as f:
                configur = yaml.safe_load(f)
            config.update(configur)
        self.config = config
        
    def load_data(self) -> None:
        ''' Request data from Spotify API
        This function initiates an HTTPS request to the Spotify API, fetching search results for the artist name "Drake" 
        along with the corresponding popularity data. Subsequently, the obtained data is stored within the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''
        CLIENT_ID = self.config['spotify_client_id']
        CLIENT_SECRET = self.config['spotify_client_secret']
        URL = 'https://accounts.spotify.com/api/token'

        auth_response = requests.post(URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        headers = {f'Authorization': 'Bearer {token}'.format(token=access_token)}
        
        try:
            data = requests.get(f'https://api.spotify.com/v1/search?query=drake&type=artist&limit=10&market=CA' , headers=headers).json()
            self.data = data            
            logging.info('Data has been loaded')
        except Exception as e:
            logging.error('Error loading Data from Spotify', exc_info=e)
            logging.error('Please check your Spotify API credentials and network connection.')

    def compute_analysis(self) -> int:
        '''Analyze previously-loaded data.
        This function runs an analytical measure mean
        and median returns an integer. And it converts the received data into a dataframe.

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : int

        '''
        artists_data = self.data['artists']['items']
        names_and_popularity = [(artist['name'], artist['popularity']) for artist in artists_data]
        # Printing the result
        for name, popularity in names_and_popularity:
            print(f'Name: {name}, Popularity: {popularity}')
        self.df = pd.DataFrame(names_and_popularity, columns=['Name', 'Popularity'])
        mean_popularity = self.df['Popularity'].mean()
        median_popularity = self.df['Popularity'].median()

        # Display the results
        print(f"Mean Popularity: {mean_popularity}")
        print(f"Median Popularity: {median_popularity}")
        return int(median_popularity)

        
    def plot_data(self, x_label='Popularity', y_label='Name', title='Popularity of Artists', save_path='output_plot.png') -> plt.Figure:
        ''' Analyze and plot data

        Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
        the path from the configuration file if not specified.

        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure

        Returns
        -------
        fig : matplotlib.Figure

        '''
        plt.barh(self.df['Name'], self.df['Popularity'], color='skyblue')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.savefig(save_path)
        plt.show()
        return plt.gcf()

    def notify_done(self, message='Your Spotify data analysis is completed.') -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Important Note
        ---------------
        You must subscribe to the specified topic name in ntfy.sh! 
        See topicname in userconfig.yml for this module's topic name.

        Parameters
        ----------
        message : str
        Text of the notification to send

        Returns
        -------
        None

        '''
        
        requests.post(f"https://ntfy.sh/{self.config['Building-robust-software-assignment']}", 
            data=message.encode(encoding='utf-8'))