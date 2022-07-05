<H1>Python Project: SpotyPy</H1>

<img src="./SpotiPy.jpg" width="300">

SpotiPy is a graph simulation of Spotify in which we have songs, which are linked together 
when a user has them added to the same playlist. 

To start the app:

1: Open a Terminal,

2: Go to the SpotyPy folder

3: Input the following into the terminal to start with our current database of songs (152,666 entries) and wait for the program to initialize
        
    "py recomendify.py spotify-mini.tsv"


4: Once the program has initialized, you can choose the following commands:

    path {origin >>>> destination}
.Finds a path between origin and destination (e.g: path Lovegame - Lady Gaga >>>> Bad Romance - Lady Gaga)

    most_added {number}

Returns songs that are present in the most amount of playlists (e.g.: most_added 10)
    
    recommended {songs/users} {ammount} {based_on}

Returns an amount of recommended users or songs based on input.

(e.g. :recommended songs 10 Lovegame - Lady Gaga >>>> Bad Romance - Lady Gaga)

    cicle {n} {origin song}

Returns a list of "n" songs, starting from the "origin song", that will loop back to the origin. 

    range {n} {song}

Returns the amount of songs that are a specified amount from said song.
(e.g: range 5 Money Honey - Lady Gaga)

    clustering (optional){song}

By default returns the average clustering coefficient for all songs. If it receives a song, it returns the clustering 
coefficient for that song. (e.g. : clustering Bad Romance - Lady Gaga)


 
