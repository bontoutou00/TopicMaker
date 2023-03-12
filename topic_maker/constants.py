'''Constants used for Topic Maker'''
from pathlib import Path
from platformdirs import user_data_dir

DATA_PATH: Path = Path(user_data_dir("TopicMaker", appauthor=False, roaming=True))
LOG_PATH: Path = Path(user_data_dir("TopicMaker", appauthor=False, roaming=True)) / "logs"
DEFAULT_TEMPLATE = '''[imdb]{
  "poster": "$poster",
  "title": "$title",
  "year": "$year",
  "directors": "$director",
  "stars": "$actors",
  "ratings": "$imdbrating",
  "votes": "$imdbvotes",
  "runTime": "$runtime",
  "summary": "$plot_full",
  "shortSummary": "$plot_short",
  "genre": "$genre",
  "releaseDate": "$released",
  "viewerRating": "$rated",
  "language": "$language",
  "imdbId": "$imdbid",
  "mediaType": "$type"
}[/imdb]
$screenshots
[mediainfo]$mediainfo[/mediainfo]
[code]
Sources:
$source
[/code]
[center][hide][b][url=$link][color=#FF0000][size=200]$link_provider[/color][/url][/b][/hide][/center]'''

VALUES_TEMPLATE = {
'iMDB | Poster link.': '$poster',
'iMDB | Title.': '$title',
'iMDB | Year.': '$year',
'iMDB | Director.': '$director',
'iMDB | Actors.': '$actors',
'iMDB | Rating formatted like "8.3".': '$imdbrating',
'iMDB | Votes.': '$imdbvotes',
'iMDB | Runtime.': '$runtime',
'iMDB | Full plot.': '$plot_full',
'iMDB | Short plot.': '$plot_short',
'iMDB | Genre.': '$genre',
'iMDB | Release date.': '$released',
'iMDB | Rated.': '$rated',
'iMDB | Language.': '$language',
'iMDB | iMDB ID.': '$imdbid',
'iMDB | Media type.': '$type',
'iMDB | Rating formatted like "8.3/10".': '$ratings_imdb',
'iMDB | Rotten Tomatoes ratings.': '$ratings_rt',
'iMDB | Metacritic reviews.': '$ratings_mc',
'MyDramaList | Name of the movie / drama.': '$title_mdl',
'MyDramaList | A link to the thumbnail.': '$thumbnail_mdl',
'MyDramaList | Drama or movie.': '$media_type_mdl',
'MyDramaList | The url that was used for scraping the data.': '$url_mdl',
'MyDramaList | Rating of the movie.': '$ratings_mdl',
'MyDramaList | Short plot of the movie / drama.': '$plot_mdl',
'MyDramaList | Actors playing in the movie / drama.': '$actors_mdl',
'MyDramaList | Native language title.': '$native_title_mdl',
'MyDramaList | Genre of the movie / drama.': '$genre_mdl',
'MyDramaList | Runtime of the movie / episode from a drama.': '$runtime_mdl',
'MyDramaList | Country of origin.': '$country_mdl',
'MyDramaList | Aliases of the movie / drama.': '$aka_mdl',
'MyDramaList | Director of the movie / drama.': '$director_mdl',
'MyDramaList | Writer of the movie / drama': '$writer_mdl',
'MyDramaList | Release date of the movie / drama.': '$release_date_mdl',
'Source': '$source',
'Link provided': '$link',
'Link provider guessed from the link provided (MEGA, Zippyshare, Google Drive, Mediafire)': '$link_provider',
'Media Info': '$mediainfo',
'Screenshots': '$screenshots',
}

VERSION = 'v1.0.0'
