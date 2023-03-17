# About

This is a simple python wrapper that can be used to download youtube videos/playlists in parallel
using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## usage

```
youtube-download [-h] -u URL [-f FORMAT] [-q QUALITY] [-b PLAYLIST_START] [-e PLAYLIST_END] [-n MAX_DOWNLOADS] [-p PATH] [-l LENGTH]
```


## options

```
  -h, --help            show this help message and exit
  -u URL, --url URL     URL of the YouTube video or playlist to download
  -f FORMAT, --format FORMAT
                        Format of the video {mp4, webm}: (default is mp4)
  -q QUALITY, --quality QUALITY
                        Quality of the video {360, 480, 720, 1080, best}: (default is best)
  -b PLAYLIST_START, --playlist-start PLAYLIST_START
                        Playlist video to start at: (default is 1)
  -e PLAYLIST_END, --playlist-end PLAYLIST_END
                        Playlist video to end at: (default is 0 for last)
  -n MAX_DOWNLOADS, --max-downloads MAX_DOWNLOADS
                        Maximum number of videos to download at once: (default is 1)
  -p PATH, --path PATH  Download path: (default is current working directory)

```
