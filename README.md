# Topic Maker
Easily create a topic with iMDB/MyDramaList infos using a template

![Topic Maker Main Window](https://user-images.githubusercontent.com/107948159/224545140-29227689-6b58-4db8-9a20-0d00819b647c.png)
![Topic Maker Template Editor Window](https://user-images.githubusercontent.com/107948159/224545174-598d013a-df3d-4414-9bf2-934e6227303c.png)


## Requirements:

* Register a new OMDB API Key here : [omdbapi.com](https://www.omdbapi.com/apikey.aspx)
* If you want to use the screenshots upload to ImgbBB you also need to register an API key here: [api.imgbb.com](https://api.imgbb.com/)
* FFmpeg in path for making screenshots if none is found

## How To Use


- Fill the 'Movie or TV Name' with your wanted search (It can be a movie / tv name but also a iMDB ID)
- If you didn't search for an iMDB ID, it will show a window with the search results
- Double click on your prefered result to continue
- It will now ask for a file to get the mediainfo
- It will produces a new txt file with the topic created

## Template values available

### IMDB
| Template Values         | Description
| ---                     | ---
| $poster                 | Poster
| $title                  | Title
| $year                   | Year.
| $director               | Director.
| $actors                 | Actors.
| $imdbrating             | Rating formatted like "8.3".
| $imdbvotes              | Votes.
| $runtime                | Runtime.
| $plot_full              | Full plot.
| $plot_short             | Short plot.
| $genre                  | Genre.
| $released               | Release date.
| $rated                  | Rated.
| $language               | Language.
| $imdbid                 | iMDB ID.
| $type                   | Media type.
| $ratings_imdb           | Rating formatted like "8.3/10".
| $ratings_rt             | Rotten Tomatoes ratings.
| $ratings_mc             | Metacritic reviews.

or return None if not found

### MyDramaList (Only if checkbutton is activated)
| Template Values         | Description
| ---                     | ---
| $title_mdl              | Name of the movie / drama.
| $thumbnail_mdl          | A link to the thumbnail.
| $media_type_mdl         | Drama or movie.
| $url_mdl                | The url that was used for scraping the data.
| $ratings_mdl            | Rating of the movie..
| $plot_mdl               | Short plot of the movie / drama.
| $casts_mdl              | Actors playing in the movie / drama.
| $native_title_mdl       | Native language title.
| $genre_mdl              | Genre of the movie / drama.
| $runtime_mdl            | Runtime of the movie / episode from a drama.
| $country_mdl            | Country of origin.
| $aka_mdl                | Aliases of the movie / drama.
| $director_mdl           | Director of the movie / drama.
| $writer_mdl             | Writer of the movie / drama.
| $release_date_mdl       | Release date of the movie / drama.


or return None if not found

### Others
| Template Values         | Description
| ---                     | ---
| $source                 | Source.
| $link                   | Link provided.
| $link_provider          | Link provider guessed from the link provided (MEGA, Zippyshare, Google Drive, Mediafire)
| $mediainfo              | Media Info.
| $screenshots            | Screenshots.

or return None if not found


You can change the 'template.txt' like you want by adding these values

## Examples

FROM:
```
[imdb]{
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
```
TO:
```
[imdb]{
  "poster": "https://m.media-amazon.com/images/M/MV5BNTA3N2Q0ZTAtODJjNy00MmQzLWJlMmItOGFmNDI0ODgxN2QwXkEyXkFqcGdeQXVyMTM0NTUzNDIy._V1_SX300.jpg",
  "title": "Morbius",
  "year": "2022",
  "directors": "Daniel Espinosa",
  "stars": "Jared Leto, Matt Smith, Adria Arjona",
  "ratings": "5.2",
  "votes": "131,421",
  "runTime": "104 min",
  "summary": "Dangerously ill with a rare blood disorder, and determined to save others suffering his same fate, Dr. Morbius attempts a desperate gamble. What at first appears to be a radical success soon reveals itself to be a remedy potentially worse than the disease.",
  "shortSummary": "Biochemist Michael Morbius tries to cure himself of a rare blood disease, but he inadvertently infects himself with a form of vampirism instead.",
  "genre": "Action, Adventure, Horror",
  "releaseDate": "01 Apr 2022",
  "viewerRating": "PG-13",
  "language": "English, Spanish, Russian",
  "imdbId": "tt5108870",
  "mediaType": "movie"
}[/imdb]
```
OR

FROM:

```
[center][size=200][b][url=$url_mdl]$title_mdl[/url][/b][/size][/center]

[center][color=#FF8000][b][size=120]$ratings_mdl[/size][/b][/color][/center]

[quote][center]$plot_mdl

[color=#FF8000][b]Title[/b][/color]: $title_mdl
[color=#FF8000][b]Original Title[/b][/color]: $native_title_mdl
[color=#FF8000][b]Also Known As[/b][/color]: $aka_mdl

[color=#FF8000][b]Type[/b][/color]: $media_type_mdl
[color=#FF8000][b]Runtime[/b][/color]: $runtime_mdl

[color=#FF8000][b]Country[/b][/color]: $country_mdl
[color=#FF8000][b]Genres[/b][/color]: $genre_mdl
```
TO:
```
[center][size=200][b][url=https://mydramalist.com/699543-the-twentieth-century-girl]20th Century Girl (2022)[/url][/b][/size][/center]

[center][color=#FF8000][b][size=120]8.6[/size][/b][/color][/center]

[quote][center]In 1999, a teen with a heart of gold begins keeping close tabs on a popular classmate as a favor to her smitten best friend.  Bo Ra is 17-year-old high school student. She is good at taekwondo and has a bright and positive personality. She is also a member of the broadcasting club at her school. Woon Ho is a member of the same broadcasting club.  Bo Ra is best friends with Yeon Du, who attends the same school. Yeon Du has a crush on Hyun Jin. She asks Bo Ra to find out everything about Hyun Jin and goes to the U.S. to have heart surgery. After that, Bo Ra begins to observe Hyun Jin closely and she falls in love with him.  (Source: Netflix, AsianWiki)  ~~ Release dates: Oct 6, 2022 (Festival) ||  Oct 21, 2022 (Netflix)

[color=#FF8000][b]Title[/b][/color]: 20th Century Girl (2022)
[color=#FF8000][b]Original Title[/b][/color]: 20세기 소녀
[color=#FF8000][b]Also Known As[/b][/color]: The Twentieth Century Girl, 20segi Sonyeo, Isibsegi Sonyeo, 이십세기 소녀

[color=#FF8000][b]Type[/b][/color]: Movie
[color=#FF8000][b]Runtime[/b][/color]: 1 hr. 59 min.

[color=#FF8000][b]Country[/b][/color]: South Korea
[color=#FF8000][b]Genres[/b][/color]: Romance, Youth, Melodrama
```

## Installation

Download the latest executable or you can compile it yourself

You can compile Pyinstaller yourself by doing:

1. Clone the Pyinstaller GitHub repo
```
git clone https://github.com/pyinstaller/pyinstaller.git
```
2. Install 'build' package with pip
``` 
pip install build
```
3. Build Pyinstaller using Python build
``` 
python -m build --sdist pyinstaller\
```
1. Install the pyinstaller package with pip
``` 
pip install pyinstaller\dist\pyinstaller-5.8.0.tar.gz
```

Command used to compile the executable:
```
pyinstaller --clean --noconfirm --onefile --windowed --name "Topic Maker v1.0.0" --icon "topic_maker/favicon.ico" --add-data "topic_maker/config.py;." --add-data "topic_maker/constants.py;." --add-data "topic_maker/exceptions.py;." --add-data "topic_maker/omdb_api_fetcher.py;." --add-data "topic_maker/template.py;." --add-data "topic_maker/favicon.ico;." --collect-data "sv_ttk" "topic_maker/main.py"
```
## Created using
* [Python](https://www.python.org/)

### Third-party modules

* [PyMDL](https://pypi.org/project/PyMDL)
* [pymediainfo](https://pypi.org/project/pymediainfo/)
* [imgbbpy](https://pypi.org/project/imgbbpy/)
### Favicon
* [Icon created by Yogi Aprelliyanto](https://www.flaticon.com/free-icon/browser_9892390)

## Virus Scan
[Virus Total](https://www.virustotal.com/gui/file/36b6d6e7ddc9f1b748b23133f7aec4802460fd413a1e6f1f8747e9b3fd04e656) - 4/69 detected

All positives detections are false (You can inspect the source code or compile it yourself)

The executable is created with Pyinstaller 5.8.0 with Python 3.11.2
(Bootloader compiled every release inside a VM, compiled because of the highest numbers of false positives in the release one)

MD5: 209b81ade42eca4cf06c1bbdf0cf8b1a

SHA-256: 36b6d6e7ddc9f1b748b23133f7aec4802460fd413a1e6f1f8747e9b3fd04e656
