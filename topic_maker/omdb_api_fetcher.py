import re
import sys
import requests
from exceptions import InvalidApiKey, NoApiKeyProvided, TooManyResults, MovieNotFound, SomethingWentWrong, IncorrectImdbId, ErrorGettingData
from config import logger

class Client:
    """Class representing a client"""
    def __init__(self, key) -> None:
        self.key = key
        self.req = requests.Session()

    def omdb_request(self, data):
        """
        The omdb_request function takes a dictionary of data and returns the response from the OMDb API.\n
        The function will raise an exception if there is no api key provided or if the api key is invalid.\n
        Args:
            data: Pass the data to be sent with the request
        Returns:
            A dictionary with the information of a movie
        """
        data_omdb = {'apikey': self.key, 'r': 'json'}
        data_omdb.update(data)
        logger.info(data_omdb)
        try:
            resp = self.req.post("https://www.omdbapi.com/", params=data_omdb, timeout=10).json()
            if resp['Response'] == 'False':
                if "Invalid API key" in resp['Error']:
                    raise InvalidApiKey(resp['Error'])
                if "No API key provided" in resp['Error']:
                    raise NoApiKeyProvided(resp['Error'])
                if "Too many results" in resp['Error']:
                    raise TooManyResults(resp['Error'])
                if "Movie not found" in resp['Error']:
                    raise MovieNotFound('Media not found!')
                if "Something went wrong" in resp['Error']:
                    raise SomethingWentWrong(resp['Error'])
                if "Incorrect IMDb ID." in resp['Error']:
                    raise IncorrectImdbId(resp['Error'])
                if "Error getting data." in resp['Error']:
                    raise ErrorGettingData(resp['Error'])
                logger.warning(resp['Error'])
                raise Exception(resp['Response'])
        except requests.exceptions.HTTPError as error:
            logger.warning(error)
        except requests.exceptions.RequestException as error:
            logger.warning(error)
        else:
            return resp

    def mediatype_imdb(self, imdbid: str):
        """
        The mediatype_imdb function accepts an IMDb ID and returns the mediatype of the associated movie or TV show.\n
        If no mediatype is found, None is returned.\n
        Args:
            imdbid: str: Pass the imdbid to the mediatype_imdb function
        Returns:
            The type of media
        """
        resp = self.omdb_request({'i': imdbid})
        try:
            mediatype = resp['Type']
        except ValueError:
            return
        logger.info(mediatype)
        return mediatype

    def mediatype_search(self, data):
        """
        The mediatype_search function takes a dictionary of data and returns the IMDb ID for that media type.\n\
        The function is called by the search_media function.\n
        Args:
            Pass the data from mediatype_search to the omdb_request function
        Returns:
            The imdb id of the movie
        """
        resp = self.omdb_request(data)
        try:
            imdbid = resp['imdbID']
        except ValueError:
            return
        else:
            logger.info(imdbid)
            return imdbid

    def movie(self, imdbid: str):
        """
        The movie function takes an imdb id and returns a dictionary of movie information.\n
        It first checks to see if the imdb id is valid, then it makes two requests to the OMDb API.\n
        The first request is for a short plot summary, while the second request is for a full plot summary.\n
        Args:
            imdbid: str: Pass the imdb id of the movie to be searched
        Returns:
            A dictionary with the movie's information
        """
        try:
            full = self.omdb_request({'i': imdbid, 'type': 'movie', 'plot': 'full'})
            short = self.omdb_request({'i': imdbid, 'type': 'movie', 'plot': 'short'})
        except IncorrectImdbId:
            sys.exit()
        else:
            resp = self.omdb_dic_handling(short, full)
            return resp

    def series(self, imdbid: str):
        """
        The series function takes an IMDb ID and returns a dictionary of the series' information.\n
        The function will return a dictionary with the following keys:\n
        Args:
            imdbid: str: Pass the imdbid of the series to be searched for
        Returns:
            A dictionary with the serie's information
        """
        try:
            full = self.omdb_request({'i': imdbid, 'type': 'series', 'plot': 'full'})
            short = self.omdb_request({'i': imdbid, 'type': 'series', 'plot': 'short'})
        except IncorrectImdbId:
            sys.exit()
        else:
            resp = self.omdb_dic_handling(short, full)
            return resp

    def omdb_dic_handling(self, short: dict, full: dict):
        """
        The omdb_dic_handling function takes two dictionaries as arguments. The first dictionary contains the short plot summary,\n
        the second contains the full plot summary. It then creates a new dictionary with all of the information from both\n
        dictionaries and returns it.\n
        Args:
            short: dict: Get the values for the columns that are not in the full parameter\n
            full: dict: Get the full plot
        Returns:
            A dictionary of the short and full plot combined
        """
        omdb_dic = {}
        for key, item in short.items():
            if item == 'N/A' and key != 'Plot' and key != 'Poster':
                omdb_dic[key.lower()] = None
            elif key == 'Ratings':
                if short['Ratings'] == []:
                    omdb_dic['ratings'] = None
                    omdb_dic['ratings_imdb'] = None
                    omdb_dic['ratings_rt'] = None
                    omdb_dic['ratings_mc'] = None
                else:
                    try:
                        omdb_dic['ratings_imdb'] = short['Ratings'][0]['Value']
                    except IndexError:
                        omdb_dic['ratings_imdb'] = None
                    try:
                        omdb_dic['ratings_rt'] = short['Ratings'][1]['Value']
                    except IndexError:
                        omdb_dic['ratings_rt'] = None
                    try:
                        omdb_dic['ratings_mc'] = short['Ratings'][2]['Value']
                    except IndexError:
                        omdb_dic['ratings_mc'] = None
            elif key == 'Plot':
                full_var = full['Plot']
                short_var = short['Plot']
                if short_var == 'N/A':
                    omdb_dic['plot_short'] = None
                    if full_var == 'N/A':
                        omdb_dic['plot_full'] = None
                    else:
                        omdb_dic['plot_full'] = re.sub(r'([\"])', r'\\\1', full_var)
                else:
                    if full_var != short_var:
                        omdb_dic['plot_full'] = re.sub(r'([\"])', r'\\\1', full_var)
                        omdb_dic['plot_short'] = re.sub(r'([\"])', r'\\\1', short_var)
                    else:
                        omdb_dic['plot_short'] = re.sub(r'([\"])', r'\\\1', short_var)
                        omdb_dic['plot_full'] = None
            elif key == 'Poster':
                if item == 'N/A':
                    omdb_dic['poster'] = "https://i.ibb.co/QmCxpVj/imdb-no-poster.png"
                else:
                    omdb_dic[key.lower()] = item
            else:
                omdb_dic[key.lower()] = item
        logger.info(omdb_dic)
        return omdb_dic
