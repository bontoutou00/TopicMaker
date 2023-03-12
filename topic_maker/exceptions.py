class InvalidApiKey(Exception):
    """ Exception when the OMDb API key is invalid. """
class NoApiKeyProvided(Exception):
    """ Exception when no OMDb API key are provided. """
class IncorrectImdbId(Exception):
    """ Exception when you search an incorrect IMDb ID. """
class TooManyResults(Exception):
    """ Exception when your search has too many results. """
class MovieNotFound(Exception):
    """ Exception when your search has no results. """
class SomethingWentWrong(Exception):
    """ Exception when something went wrong. """
class ErrorGettingData(Exception):
    """ Exception when getting data. """
