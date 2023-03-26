import subprocess
import archiver
import json
import os

'''
schedule_configs objects are pairs of configurations as dicts:
    the download config
        and
    the schedule config
'''
class schedule_config(tuple):
    def __new__(cls, ydl_opts=None, sched_opts=None):
        '''
        ydl_opts based on https://github.com/ytdl-org/youtube-dl/blob/master/README.md#options
        sched_opts based on Windows Task Scheduler XML exports
        
            - values default to None
            - keys are named such that inserting two dashes in front (--) provides CLI flags
              for running youtube-dl in subprocess of archiver.py
        '''
        if ydl_opts == None:
            ydl_opts = {
                # MISC OPTIONS
                'version': None, # print program version and exit
                'update': None, # update ytdl to the latest version, given sufficient permissions
                'ignore-errors': None, # continue on download errors, for example to skip unavailable videos in a playlist
                'abort-on-error': None, # abort downloading of further videos (in the playlist or the command line) if an error occurs
                'default-search': None, 
                                        # Use this prefix for unqualified URLs.
                                        # For example "gvsearch2:" downloads two
                                        # videos from google videos for youtube-
                                        # dl "large apple". Use the value "auto"
                                        # to let youtube-dl guess ("auto_warning"
                                        # to emit a warning when guessing).
                                        # "error" just throws an error. The
                                        # default value "fixup_error" repairs
                                        # broken URLs, but emits an error if this
                                        # is not possible instead of searching.
                                        
                'ignore-config': None, # do not read configuration files.
                'config-location': None, # location of the configuration file; either the path to the config or its containing directory
                'flat-playlist': None, # do not extract the videos of a playlist, only list them
                'mark-watched': None, # Youtube only
                'no-mark-watched': None, # Youtube only

                # NETWORK OPTIONS
                'proxy': None, 
                                # Use the specified HTTP/HTTPS/SOCKS
                                # proxy. To enable SOCKS proxy, specify a
                                # proper scheme. For example
                                # socks5://127.0.0.1:1080/. Pass in an
                                # empty string (--proxy "") for direct
                                # connection
                                
                'socket-timeout': None, # time to wait before giving up, in seconds
                'source-address': None, # client-side IP address to bind to
                'force-ipv4': None, # make all connections via IPv4
                'force-ipv6': None, # make all connections via IPv6

                # GEO RESTRICTION OPTIONS

                # VIDEO SELECTION OPTIONS
                'playlist-start': None, # playlist video to start at
                'playlist-end': None, # playlist video to end at
                'playlist-items': None, # playlist video items to download, specified as tuple of indices and ranges
                'match-title': None, # download only matching titles by regex or caseless substring
                'reject-title': None, # Skip download for matching titles by regex or caseless substring
                'max-downloads': None, # Abort after downloading specfied number of files
                'min-filesize': None, # do not downlaod any videos smaller than specified (e.g. 50k or 44.6m)
                'max-filesize': None, # do not download any videos larger than specified (e.g. 50k or 44.6m)
                'date': None, # download only videos uploaded on the specified date
                'datebefore': None, # download only videos uploaded on or before this date (inclusive)
                'dateafter': None, # download only videos uploaded on or after this date (inclusive)
                'min-views': None, # do not download any videos with less than the specified view count
                'max-views': None, # do not download any videos with more than the specified view count
                'match-filter': None, 
                                        # Generic video filter. Specify any key
                                        # (see the "OUTPUT TEMPLATE" for a list
                                        # of available keys) to match if the key
                                        # is present, !key to check if the key is
                                        # not present, key > NUMBER (like
                                        # "comment_count > 12", also works with
                                        # >=, <, <=, !=, =) to compare against a
                                        # number, key = 'LITERAL' (like "uploader
                                        # = 'Mike Smith'", also works with !=) to
                                        # match against a string literal and & to
                                        # require multiple matches. Values which
                                        # are not known are excluded unless you
                                        # put a question mark (?) after the
                                        # operator. For example, to only match
                                        # videos that have been liked more than
                                        # 100 times and disliked less than 50
                                        # times (or the dislike functionality is
                                        # not available at the given service),
                                        # but who also have a description, use
                                        # --match-filter "like_count > 100 &
                                        # dislike_count <? 50 & description" .
                                        
                'no-playlist': None, # download only the video, if the specified URL refers to a video and a playlist
                'yes-playlist': None, # download the playlist, if the specified URL refers to a video and a playlist
                'age-limit': None, # download only videos suitable for the given age
                'download-archive': None, # download videos not listed in the archive file. Record the IDs of all downloaded videos in the archive file
                'include-ads': None, # download advertisements as well (experimental)

                # DOWNLOAD OPTIONS
                'limit-rate': None, # maximum download rate in bytes per second (e.g. 50K or 4.2M)
                'retries': None, # number of retries (default is 10), or "infinite"
                'fragment-retries': None, # number of retries for a fragment (default is 10), or "infinite" (DASH, hlsnative, and ISM)
                'skip-unavailable': None, # Skip unavailable fragments (DASH, hlsnative, and ISM)
                'abort-on-unavailable-fragment': None, # abort downloading when some fragment is not available
                'keep-fragments': None, # keep downloaded fragments on disk after downloading is finished; fragments are erased by default
                'buffer-size': None, # size of download buffer (e.g. 1024 or 16K) (default is 1024)
                'no-resize-buffer': None, # do not automatically adjust the buffer size. By default, the buffer size is automatically resized from the initial value
                'http-chunk-size': None, # size of a chunk for chunk-based HTTP downloading (e.g. 10485760 or 10M) (default is disabled). May be useful for bypassing bandwidth throttling imposed by a webserver (experimental)
                'playlist-reverse': None, # download playlist videos in reverse order
                'playlist-random': None, # download playlist videos in random order
                'xattr-set-filesize': None, # set file xattribute ytdl.filesize with expected file size
                'hls-prefer-native': None, # use the native HLS downloader instead of ffmpeg
                'hls-prefer-ffmpeg': None, # use ffmpeg instead of the native HLS downloader
                'hls-use-mpegts': None, # use the mpegts container for HLS videos, allowing to play the video while downloading (some players may not be able to play it)
                'external-downloader': None, # use the specified external downloader. Currently supports: (aria2c, avconv, axel, curl, ffmpeg, httpie, wget)
                'external-downloader-args': None, # give these arguments to the external downloader

                # FILESYSTEM OPTIONS
                'batch-file': None, # file containing URLs to download ("-" for stdin), one URL per line. Lines starting with "#", ";", or "]" are considered as comments and ignored.
                'id': None, # use only video ID in file name
                'output': None, # output filename template, see the "OUTPUT TEMPLATE" for all the info
                'output-na-placeholder': None, # placeholder value for unavailable meta fields in output filename template (default is "NA")
                'autonumber-start': None, # specify the start value for %(autonumber)s (default is 1)
                'restrict-filenames': None, # restrict filenamess to only ASCII characters, and avoid "&" and spaces in filenames
                'no-overwrites': None, # do not overwrite files
                'continue': None, # force resume of partially downloaded files. By default, youtube-dl will resume downloads if possible.
                'no-continue': None, # do not resume partially downloaded files (restart from beginning)
                'no-part': None, # do not use .part files - write directly into output file
                'no-mtime': None, # do not use the last-modified header to set the file modification time
                'write-description': None, # write video description to a .description file
                'write-info-json': None, # write video metadata to a .info.json file
                'write-annotations': None, # write video annotations to a annotations.xml file
                'load-info-json': None, # provide destination JSON file containing the video information (created with the "--write-info-json" option)
                'cookies': None, # file to read cookies from and dump cookie jar in
                'cache-dir': None, 
                                    # Location in the filesystem where
                                    # youtube-dl can store some downloaded
                                    # information permanently. By default
                                    # $XDG_CACHE_HOME/youtube-dl or
                                    # ~/.cache/youtube-dl . At the moment,
                                    # only YouTube player files (for videos
                                    # with obfuscated signatures) are cached,
                                    # but that may change.
                                    
                'no-cache-dir': None, # disable filesystem caching
                'rm-cache-dir': None, # delete all filesystem cache files

                # THUMBNAIL OPTIONS
                'write-thumbnail': None, # write thumbnail image to disk
                'write-all-thumbnails': None, # write all thumbnail image formats to disk
                'list-thumbnails': None, # simulate and list all available thumbnail formats

                # SIMULATION OPTIONS

                # WORKAROUND OPITONS

                # VIDEO FORMAT OPTIONS
                'format': None, # video format code, see the "FORMAT SELECTION" for all the info
                'all-formats': None, # download all available video formats
                'prefer-free-formats': None, # prefer free video formats unless a specific one is requested
                'list-formats': None, # list all available formats of requested videos
                'youtube-skip-dash-manifest': None, # do not download the DASH manifest and related data on Youtube videos
                'merge-output-format': None, # if a merge is required (e.g. bestvideo+bestaudio), output to specified container format. One of mkv, mp4, ogg, webm, flv. Ignored if no merge is required

                # SUBTITLE OPTIONS
                'write-sub': None, # write subtitle file
                'write-auto-sub': None, # write automatically generated subtitle file (YouTube only)
                'all-subs': None, # download all the available subtitles of the video
                'list-subs': None, # list all available subtitles for the video
                'sub-format': None, # specify subtitle format, accepts formats preference, for example: "srt" or "ass/srt/best"
                'sub-lan': None, # languages of the subtitles to download (optional) separated by commas, use --list-subs for available language tags

                # AUTHENTICATION OPTIONS
                'username': None, # login with this account ID
                'password': None, # account password. If this option is left out, youtube-dl will ask interactively
                'twofactor': None, # specify two-factor authentication code
                'netrc': None, # specify .netrc authentication data
                'video-password': None, # specify video password (vimeo, youku)

                # ADOBE PASS OPTIONS
                'ap-mso': None, # specify Adobe Pass multiple-system operator (TV provider) identifier, user --ap-list-mso for a list of available MSOs
                'ap-username': None, # specify Multiple-system operator account login
                'ap-password': None, # specify Multiple-system operator account password. If this option is left out, youtube-dl will ask interactively.
                'ap-list-mso': None, # list all support multiple-system operators

                # POST-PROCESSING OPTIONS
                'extract-audio': None, # convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe)
                'audio-format': None, # specify audio format: "best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", or "wav"; "best" by default; No effect without --extract-audio
                'audio-quality': None, # specify ffmpeg/avconv audio quality, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)
                'recode-video': None, # specify whether to encode the video to another format (currently supported: mp4|flv|ogg|webm|mkv|avi)
                'postprocessor-args': None, # specify argument to give to the postprocessor
                'keep-video': None, # keep the video file on disk after the post-processing; the video is erased by default
                'no-post-overwrites': None, # do not overwrite post-processed files; the post-processed files are overwritten by default
                'embed-subs': None, # embed subtitles in the video (only for mp4, webm, and mkv videos)
                'embed-thumbnail': None, # embed thumbnail in the audio as cover art
                'add-metadata': None, # write metadata to the video file
                'metadata-from-title': None,
                                            # Parse additional metadata like song
                                            # title / artist from the video title.
                                            # The format syntax is the same as
                                            # --output. Regular expression with named
                                            # capture groups may also be used. The
                                            # parsed parameters replace existing
                                            # values. Example: --metadata-from-title
                                            # "%(artist)s - %(title)s" matches a
                                            # title like "Coldplay - Paradise".
                                            # Example (regex): --metadata-from-title
                                            # "(?P<artist>.+?) - (?P<title>.+)"
                                            
                'xattrs': None, # write metadata to the video file's xattrx (using dublin core and xdg standards)
                'fixup': None, # automatically correct known faults of the file. One of never (do nothing), warn (only emit a warning), detect_or_warn (the default; fix file if we can, warn otherwise)
                'prefer-avconv': None, # prefer avconv over ffmpeg for running postprocessors
                'prefer-ffmpeg': None, # prefer ffmpeg over avconv for running the postprocessors (default)
                'ffmpeg-location': None, # location of the ffmpeg/avconv binary; either the path to the binary or its containing directory
                'exec': None, # execute a command on the file after downloading and post-processing, similar to find's -exec syntax. Example: --exec "adb push {} /sdcard/Music/ && rm{}"
                'convert-subs': None # convert the subtitles to other format (currently supported: srt|ass|vtt|lrc)
        }
        elif not isinstance(ydl_opts, dict): # manage passing non-dict to __new__
            raise Exception('schedule_config __new__ method received arguments which were not dictionaries')
        if (sched_opts == None):
            sched_opts = {
                'task': {
                    'registration-info': {
                        'date': None, # task creation date
                        'author': None, # task author
                        'URI': None, # identifier for the task
                    },
                    'triggers': {},
                    'principals': {
                        'principal': {
                            'user-id': None # user id under whose permissions the task will be run
                        }
                    },
                    'settings': {
                        'enabled': True, # enable the task to run when triggered
                        'allow-start-on-demand': True, # allow the user to run the program on demand
                        'allow-hard-terminate': True # allow the user to end the task while it is running
                    },
                    'actions': {
                        'exec': {
                            'command': None # the command to be executed by the windows task scheduler
                        }
                    }
                }
            }
        elif not isinstance(sched_opts, dict): # manage passing non-dict to __new__
            raise Exception('schedule_config __new__ method received arguments which were not dictionaries')

        self = super(schedule_config, cls).__new__(cls, [ydl_opts, sched_opts])

        return self
    
    def __str__(self):
        return json.dumps(self[0], indent=4) + '\n\n' + json.dumps(self[1], indent=4)
    
    def ydl_profile(self):
        return self[0]
    
    def sched_profile(self):
        return self[1]

    # Make a video archive schedule
    def make_schedule(username, password):
        xml_path = os.path.abspath(
            os.path.join(os.path.split(os.path.dirname(archiver.__file__))[0],
                        './settings/xml/vb_archiver.xml'))
        task_name = 'vb_archiver'
        task_command = ['schtasks.exe',
                        '/Create',
                        '/RU', username,
                        '/RP', password,
                        '/TN', task_name,
                        '/XML', xml_path]
        subprocess.run(task_command)

    # Export data to be used in another file
    def contents():
        output_path = os.path.abspath(
            os.path.join(os.path.dirname(archiver.__file__), '../dldest/filenames.txt') )
        url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
        args = [
            'youtube-dl',
            url,
            '--config-location', os.path.abspath(
                os.path.join(os.path.split(os.path.dirname(archiver.__file__))[0],
                        './settings/ytdl.conf')),
            '--yes-playlist']
        return {'args': args, 'output_path': output_path}


current = schedule_config()

if (__name__ == '__main__'):
    print(current)
    #current.make_schedule(os.getenv('username'), 'mynameisjoe1')
