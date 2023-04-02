from schema import Schema, Optional, Use, And, Or
from vba.py.lib.deepdict import deepdict
import os
import re

SYSTEM_ID = 'S-1-5-18' # Windows Task Scheduler "SYSTEM" user-id

# https://stackoverflow.com/questions/66140495/python-how-to-check-the-string-is-a-utc-timestamp
# regex pattern to confirm ISO8601 format conformity from time strings, primarily for task scheduling
# validates "yyyy-(m)m-(d)dT(h)h:(m)m:(s)s.s(ssssss)"
DATETIME_ISO8601_PATTERN = re.compile(
    r'^([0-9]{4})' r'-' r'([0-9]{1,2})' r'-' r'([0-9]{1,2})' # date
    r'([T\s][0-9]{1,2}:[0-9]{1,2}:?[0-9]{1,2}(\.[0-9]{1,7})?)?' # time
)

# TODO: adjust regex to conform to XML duration datatype format
# https://learn.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-deadline-element
# attempt at creating regex pattern to confirm duration type conformity in XML elements
# validates "P(nY)(nM)(nD)T(nH)(nM)(nS)" such that the minimum input is P1M (1 minute duration)
XML_DURATION_PATTERN = re.compile(
    r'P([123]Y)?' r'([01]?[012]M)?' r'([123]?[0-9]?[0-9]D)?' # date
    r'T?([0-7]?[0-9]H)?' r'([012]?[0-9]?[0-9]M)?' r'([012]?[0-9]?[0-9]S)?' # time
)

'''
ydl_opts based on https://github.com/ytdl-org/youtube-dl/blob/master/README.md#options
sched_opts based on Windows Task Scheduler XML exports

    - All keys are optional, as the schema is an analog to a command line executable's options
    - Keys are named such that inserting two dashes in front (--) provides CLI flags
        for running youtube-dl in subprocess of archiver.py
    - Comments beneath key:value pairs describe behavior of option if inputted on command line
'''
YDL_SCHEMA = Schema(
    {
        # MISC OPTIONS
        Optional('version'): True,
        # print program version and exit
        Optional('update'): True,
        # update ytdl to the latest version, given sufficient permissions
        Optional('ignore-errors'): True,
        # continue on download errors, for example to skip unavailable videos in a playlist
        Optional('abort-on-error'): True,
        # abort downloading of further videos (in the playlist or the command line) if an error occurs
        Optional('default-search'): str, 
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
                                
        Optional('ignore-config'): True,
        # do not read configuration files.
        Optional('config-location'): And(str, os.path.exists),
        # location of the configuration file; either the path to the config or its containing directory
        Optional('flat-playlist'): True,
        # do not extract the videos of a playlist, only list them
        Optional(Or('mark-watched', 'no-mark-watched')): True,
        # Youtube only

        # NETWORK OPTIONS
        Optional('proxy'): str, 
                        # Use the specified HTTP/HTTPS/SOCKS
                        # proxy. To enable SOCKS proxy, specify a
                        # proper scheme. For example
                        # socks5://127.0.0.1:1080/. Pass in an
                        # empty string (--proxy "") for direct
                        # connection
                        
        Optional('socket-timeout'): Use(int),
        # time to wait before giving up, in seconds
        Optional('source-address'): str,
        # client-side IP address to bind to
        Optional(Or('force-ipv4', 'force-ipv6')): True,
        # make all connections via IPv4 or via IPv6

        # GEO RESTRICTION OPTIONS

        # VIDEO SELECTION OPTIONS
        Optional('playlist-start'): Use(int),
        # playlist video index to start at
        Optional('playlist-end'): Use(int),
        # playlist video index to end at
        Optional('playlist-items'): str,
        # playlist video items to download, specified as tuple of indices and ranges
        Optional('match-title'): str,
        # download only matching titles by regex or caseless substring
        Optional('reject-title'): str,
        # Skip download for matching titles by regex or caseless substring
        Optional('max-downloads'): Use(int),
        # Abort after downloading specfied number of files
        Optional('min-filesize'): str,
        # do not downlaod any videos smaller than specified (e.g. 50k or 44.6m)
        Optional('max-filesize'): str,
        # do not download any videos larger than specified (e.g. 50k or 44.6m)
        Optional('date'): str,
        # download only videos uploaded on the specified date
        Optional('datebefore'): str,
        # download only videos uploaded on or before this date (inclusive)
        Optional('dateafter'): str,
        # download only videos uploaded on or after this date (inclusive)
        Optional('min-views'): Use(int),
        # do not download any videos with less than the specified view count
        Optional('max-views'): Use(int),
        # do not download any videos with more than the specified view count
        Optional('match-filter'): str, 
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
                                
        Optional(Or('no-playlist', 'yes-playlist')): True,
        # download only the video or the whole playlist, if the specified URL refers to a video and a playlist
        Optional('age-limit'): True,
        # download only videos suitable for the given age
        Optional('download-archive'): True,
        # download videos not listed in the archive file. Record the IDs of all downloaded videos in the archive file
        Optional('include-ads'): True,
        # download advertisements as well (experimental)

        # DOWNLOAD OPTIONS
        Optional('limit-rate'): str,
        # maximum download rate in bytes per second (e.g. 50K or 4.2M)
        Optional('retries'): Or(And(Use(int), lambda n: 0 <= n), 'infinite'),
        # number of retries (default is 10), or "infinite"
        Optional('fragment-retries'): Or(And(Use(int), lambda n: 0 <= n), 'infinite'),
        # number of retries for a fragment (default is 10), or "infinite" (DASH, hlsnative, and ISM)
        Optional('skip-unavailable'): True,
        # Skip unavailable fragments (DASH, hlsnative, and ISM)
        Optional('abort-on-unavailable-fragment'): True,
        # abort downloading when some fragment is not available
        Optional('keep-fragments'): True,
        # keep downloaded fragments on disk after downloading is finished; fragments are erased by default
        Optional('buffer-size'): str,
        # size of download buffer (e.g. 1024 or 16K) (default is 1024)
        Optional('no-resize-buffer'): True,
        # do not automatically adjust the buffer size. By default, the buffer size is automatically resized from the initial value
        Optional('http-chunk-size'): str,
        # size of a chunk for chunk-based HTTP downloading (e.g. 10485760 or 10M) (default is disabled). May be useful for bypassing bandwidth throttling imposed by a webserver (experimental)
        Optional(Or('playlist-reverse', 'playlist-random')): True,
        # download playlist videos in reverse or random order
        Optional('xattr-set-filesize'): True,
        # set file xattribute ytdl.filesize with expected file size
        Optional(Or('hls-prefer-native', 'hls-prefer-ffmpeg')): True,
        # use the native HLS downloader instead of ffmpeg or use ffmpeg instead of the native HLS downloader
        Optional('hls-use-mpegts'): True,
        # use the mpegts container for HLS videos, allowing to play the video while downloading (some players may not be able to play it)
        Optional('external-downloader'): str,
        # use the specified external downloader. Currently supports: (aria2c, avconv, axel, curl, ffmpeg, httpie, wget)
        Optional('external-downloader-args'): str,
        # give these arguments to the external downloader

        # FILESYSTEM OPTIONS
        Optional('batch-file'): And(str, os.path.exists),
        # file containing URLs to download ("-" for stdin), one URL per line. Lines starting with "#", ";", or "]" are considered as comments and ignored.
        Optional('id'): True,
        # use only video ID in file name
        Optional('output'): str,
        # output filename template, see the "OUTPUT TEMPLATE" for all the info
        Optional('output-na-placeholder'): str,
        # placeholder value for unavailable meta fields in output filename template (default is "NA")
        Optional('autonumber-start'): Use(int),
        # specify the start value for %(autonumber)s (default is 1)
        Optional('restrict-filenames'): True,
        # restrict filenamess to only ASCII characters, and avoid "&" and spaces in filenames
        Optional('no-overwrites'): True,
        # do not overwrite files
        Optional(Or('continue', 'no-continue')): True,
        # force resume of partially downloaded files. By default, youtube-dl will resume downloads if possible.
        # OR do not resume partially downloaded files (restart from beginning)
        Optional('no-part'): True, 
        # do not use .part files
        Optional('no-mtime'): True,
        # do not use the last-modified header to set the file modification time
        Optional('write-description'): True,
        # write video description to a .description file
        Optional('write-info-json'): True,
        # write video metadata to a .info.json file
        Optional('write-annotations'): True,
        # write video annotations to a annotations.xml file
        Optional('load-info-json'): And(str, os.path.exists),
        # provide destination JSON file containing the video information (created with the "--write-info-json" option)
        Optional('cookies'): And(str, os.path.exists),
        # file to read cookies from and dump cookie jar in
        Optional('cache-dir'): And(str, os.path.exists), 
                            # Location in the filesystem where
                            # youtube-dl can store some downloaded
                            # information permanently. By default
                            # $XDG_CACHE_HOME/youtube-dl or
                            # ~/.cache/youtube-dl . At the moment,
                            # only YouTube player files (for videos
                            # with obfuscated signatures) are cached,
                            # but that may change.
                            
        Optional('no-cache-dir'): True,
        # disable filesystem caching
        Optional('rm-cache-dir'): True,
        # delete all filesystem cache files

        # THUMBNAIL OPTIONS
        Optional('write-thumbnail'): True,
        # write thumbnail image to disk
        Optional('write-all-thumbnails'): True,
        # write all thumbnail image formats to disk
        Optional('list-thumbnails'): True,
        # simulate and list all available thumbnail formats

        # SIMULATION OPTIONS

        # WORKAROUND OPITONS

        # VIDEO FORMAT OPTIONS
        Optional('format'): str,
        # video format code, see the "FORMAT SELECTION" for all the info
        Optional('all-formats'): True,
        # download all available video formats
        Optional('prefer-free-formats'): True,
        # prefer free video formats unless a specific one is requested
        Optional('list-formats'): True,
        # list all available formats of requested videos
        Optional('youtube-skip-dash-manifest'): True,
        # do not download the DASH manifest and related data on Youtube videos
        Optional('merge-output-format'): str,
        # if a merge is required (e.g. bestvideo+bestaudio), output to specified container format. One of mkv, mp4, ogg, webm, flv. Ignored if no merge is required

        # SUBTITLE OPTIONS
        Optional('write-sub'): True,
        # write subtitle file
        Optional('write-auto-sub'): True,
        # write automatically generated subtitle file (YouTube only)
        Optional('all-subs'): True,
        # download all the available subtitles of the video
        Optional('list-subs'): True,
        # list all available subtitles for the video
        Optional('sub-format'): str,
        # specify subtitle format, accepts formats preference, for example: "srt" or "ass/srt/best"
        Optional('sub-lan'): str,
        # languages of the subtitles to download (optional) separated by commas, use --list-subs for available language tags

        # AUTHENTICATION OPTIONS
        Optional('username'): str,
        # login with this account ID
        Optional('password'): str,
        # account password. If this option is left out, youtube-dl will ask interactively
        Optional('twofactor'): str,
        # specify two-factor authentication code
        Optional('netrc'): str,
        # specify .netrc authentication data
        Optional('video-password'): str,
        # specify video password (vimeo, youku)

        # ADOBE PASS OPTIONS
        Optional('ap-mso'): str,
        # specify Adobe Pass multiple-system operator (TV provider) identifier, user --ap-list-mso for a list of available MSOs
        Optional('ap-username'): str,
        # specify Multiple-system operator account login
        Optional('ap-password'): str,
        # specify Multiple-system operator account password. If this option is left out, youtube-dl will ask interactively.
        Optional('ap-list-mso'): str,
        # list all support multiple-system operators

        # POST-PROCESSING OPTIONS
        Optional('extract-audio'): True,
        # convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe)
        Optional('audio-format'): str,
        # specify audio format: "best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", or "wav"; "best" by default; No effect without --extract-audio
        Optional('audio-quality'): Or(And(Use(int), lambda n: 0 <= n <= 9), str),
        # specify ffmpeg/avconv audio quality, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)
        Optional('recode-video'): str,
        # specify whether to encode the video to another format (currently supported: mp4|flv|ogg|webm|mkv|avi)
        Optional('postprocessor-args'): str,
        # specify argument to give to the postprocessor
        Optional('keep-video'): True,
        # keep the video file on disk after the post-processing; the video is erased by default
        Optional('no-post-overwrites'): True,
        # do not overwrite post-processed files; the post-processed files are overwritten by default
        Optional('embed-subs'): True,
        # embed subtitles in the video (only for mp4, webm, and mkv videos)
        Optional('embed-thumbnail'): True,
        # embed thumbnail in the audio as cover art
        Optional('add-metadata'): True,
        # write metadata to the video file
        Optional('metadata-from-title'): True,
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
                                    
        Optional('xattrs'): True,
        # write metadata to the video file's xattrx (using dublin core and xdg standards)
        Optional('fixup'): str,
        # automatically correct known faults of the file. One of 'never' (do nothing), 'warn' (only emit a warning), 'detect_or_warn' (the default; fix file if we can, warn otherwise)
        Optional('prefer-avconv'): True,
        # prefer avconv over ffmpeg for running postprocessors
        Optional('prefer-ffmpeg'): True,
        # prefer ffmpeg over avconv for running the postprocessors (default)
        Optional('ffmpeg-location'): And(str, os.path.exists),
        # location of the ffmpeg/avconv binary; either the path to the binary or its containing directory
        Optional('exec'): str,
        # execute a command on the file after downloading and post-processing, similar to find's -exec syntax. Example: --exec "adb push {} /sdcard/Music/ && rm{}"
        Optional('convert-subs'): str
        # convert the subtitles to other format (currently supported: srt|ass|vtt|lrc)
    }
)

XML_SCHEMA = Schema(
    {
        'registration-info': {
            'date': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))), # task creation date is in ISO8601 Time Format
            'author': str, # task author
            'URI': str, # identifier for the task
            Optional('description'): str,
            Optional('documentation'): str,
            Optional('security-descriptor'): str,
            Optional('source'): str,
            Optional('version'): str
        },
        'triggers': And({
            Optional('boot-trigger') : {
                'delay': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration)))
            },
            Optional('calendar-trigger'): {
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                },
                Optional('schedule-by-day'): {
                    'days-interval': And(Use(int), lambda n: 0 <= n <= 255)
                },
                Optional('schedule-by-month'): {
                    'days-of-month': And(Use(int), lambda n: 0 <= n <= 31),
                    'months': { # https://learn.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-schedulebymonth-calendartriggertype-element
                        Optional('January'): '',
                        Optional('February'): '',
                        Optional('March'): '',
                        Optional('April'): '',
                        Optional('May'): '',
                        Optional('June'): '',
                        Optional('July'): '',
                        Optional('August'): '',
                        Optional('September'): '',
                        Optional('October'): '',
                        Optional('November'): '',
                        Optional('December'): ''
                    }
                },
                Optional('schedule-by-month-day-of-week'): {
                    'days-of-week': { # days-of-week and months suffer the same issue as months in 'schedule-by-month' dict value
                        Optional('Monday'): '',
                        Optional('Tuesday'): '',
                        Optional('Wednesday'): '',
                        Optional('Thursday'): '',
                        Optional('Friday'): '',
                        Optional('Saturday'): '',
                        Optional('Sunday'): ''
                    },
                    'months': {
                        Optional('January'): '',
                        Optional('February'): '',
                        Optional('March'): '',
                        Optional('April'): '',
                        Optional('May'): '',
                        Optional('June'): '',
                        Optional('July'): '',
                        Optional('August'): '',
                        Optional('September'): '',
                        Optional('October'): '',
                        Optional('November'): '',
                        Optional('December'): ''
                    },
                    'weeks': And(Use(int), lambda n: 0 <= n <= 255)
                },
                Optional('schedule-by-week'): {
                    'days-of-week': {
                        Optional('Monday'): '',
                        Optional('Tuesday'): '',
                        Optional('Wednesday'): '',
                        Optional('Thursday'): '',
                        Optional('Friday'): '',
                        Optional('Saturday'): '',
                        Optional('Sunday'): ''
                    },
                    'weeks-interval': And(Use(int), lambda n: 0 <= n <= 255)
                }
            },
            Optional('event-trigger'): {
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('delay'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                },
                Optional('subscription'): [] # seems complicated https://learn.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-eventtrigger-triggergroup-element
            },
            Optional('idle-trigger'): {
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                }
            },
            Optional('logon-trigger'): {
                'user-id': And(str, lambda s: len(s) > 0),
                'delay': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                }
            },
            Optional('registration-trigger'): {
                'delay': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                }
            },
            Optional('time-trigger'): {
                'end-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                'start-boundary': And(str, lambda date: bool(re.fullmatch(DATETIME_ISO8601_PATTERN, date))),
                Optional('enabled', default=True): bool,
                Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('repetition'): {
                    'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                    Optional('duration'): Or(And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))), None),
                    Optional('stop-at-duration-end'): bool
                }
            },
        }, lambda trig_dict: len(trig_dict) == 1), # And method ensures only one trigger is present
        'principals': And([{
            'principal': {
                Or('user-id', 'group-id', only_one=True): And(str, lambda s: len(s) > 0), # user id under whose permissions the task will be run
                Optional('display-name'): str,
                Optional('logon-type'): Or('S4U', 'Password', 'InteractiveToken'),
                Optional('process-token-sid-type'): Or(And(str, lambda s: len(s) > 0), None),
                Optional('required-privileges'): 'SeCreateTokenPrivilege',
                Optional('run-level'): Or('LeastPrivilege', 'HighestAvailable')
            }
        }], lambda princ_list: 1 <= len(princ_list) <= 32),
        'settings': {
            Optional('enabled', default=True): bool, # enable the task to run when triggered
            Optional('allow-start-on-demand', default=True): bool, # allow the user to run the program on demand
            Optional('allow-hard-terminate', default=True): bool, # allow the user to end the task while it is running
            Optional('delete-expired-task-after'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
            Optional('disallow-start-if-on-batteries', default=False): bool, # default to false to counteract Task Scheduler defaults
            Optional('execution-time-limit'): And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
            Optional('hidden', default=False): bool,
            Optional('idle-settings'): {
                'stop-on-idle-end': bool,
                'restart-on-idle': bool
            },
            Optional('maintenance-settings'): {
                'deadline': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                'period': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                Optional('exclusive'): bool
            },
            Optional('multiple-instances-policy'): Or('Parallel', 'Queue', 'IgnoreNew', 'StopExisting'),
            Optional('priority'): And(Use(int), lambda n: 0 <= n <= 10),
            Optional('restart-on-failure'): {
                'interval': And(str, lambda duration: bool(re.fullmatch(XML_DURATION_PATTERN, duration))),
                'count': And(Use(int), lambda n: 0 <= n <= 255)
            },
            Optional('run-only-if-idle', default=False): bool,
            Optional('run-only-if-network-available', default=True): bool,
            Optional('start-when-available'): bool,
            Optional('stop-if-going-on-batteries', default=False): bool,
            Optional('volatile'): bool,
            Optional('wake-to-run'): bool
        },
        'actions': {
            'exec': {
                'command': And(str, os.path.exists) # the command to be executed by the windows task scheduler
            }
        }
    }
)


'''
ydl_opts based on https://github.com/ytdl-org/youtube-dl/blob/master/README.md#options
sched_opts based on Windows Task Scheduler XML exports

    - Details on each key's usage described in YDL_SCHEMA, or github link above
'''
BASE_YDL_OPTS = deepdict(dict.fromkeys(['version', 'update', 'ignore-errors', 'abort-on-error',
                               'default-search', 'ignore-config', 'config-location',
                               'flat-playlist', 'mark-watched', 'no-mark-watched', 'proxy',
                               'socket-timeout', 'source-address', 'force-ipv4', 'force-ipv6',
                               'playlist-start', 'playlist-end', 'playlist-items', 'match-title',
                               'reject-title', 'max-downloads', 'min-filesize', 'max-filesize',
                               'date', 'datebefore', 'dateafter', 'min-views', 'max-views',
                               'match-filter', 'no-playlist', 'yes-playlist', 'age-limit',
                               'download-archive', 'include-ads', 'limit-rate', 'retries',
                               'fragment-retries', 'skip-unavailable', 'abort-on-unavailable-fragment',
                               'keep-fragments', 'buffer-size', 'no-resize-buffer',
                               'http-chunk-size', 'playlist-reverse', 'playlist-random',
                               'xattr-set-filesize', 'hls-prefer-native', 'hls-prefer-ffmpeg',
                               'hls-use-mpegts', 'external-downloader', 'external-downloader-args',
                               'batch-file', 'id', 'output', 'output-na-placeholder',
                               'autonumber-start', 'restrict-filenames', 'no-overwrites',
                               'continue', 'no-continue', 'no-part', 'no-mtime', 'write-description',
                               'write-info-json', 'write-annotations', 'load-info-json', 'cookies',
                               'cache-dir', 'no-cache-dir', 'rm-cache-dir', 'write-thumbnail',
                               'write-all-thumbnails', 'list-thumbnails', 'format', 'all-formats',
                               'prefer-free-formats', 'list-formats', 'youtube-skip-dash-manifest',
                               'merge-output-format', 'write-sub', 'write-auto-sub', 'all-subs',
                               'list-subs', 'sub-format', 'sub-lan', 'username', 'password',
                               'twofactor', 'netrc', 'video-password', 'ap-mso', 'ap-username',
                               'ap-password', 'ap-list-mso', 'extract-audio', 'audio-format',
                               'audio-quality', 'recode-video', 'postprocessor-args', 'keep-video',
                               'no-post-overwrites', 'embed-subs', 'embed-thumbnail', 'add-metadata',
                               'metadata-from-title', 'xattrs', 'fixup', 'prefer-avconv', 'prefer-ffmpeg',
                               'ffmpeg-location', 'exec', 'convert-subs']))

BASE_SCHED_OPTS = deepdict({
    'registration-info': {
        'date': None, # task creation date
        'author': None, # task author
        'URI': None, # identifier for the task
    },
    'triggers': {
            'calendar-trigger': {
                    'start-boundary': None,
                    'end-boundary': None,
                    'repetition': {
                        'interval': None
                    }
            }
        },
    'principals': [{
        'principal': {
            'user-id': None # user id under whose permissions the task will be run
        }
    }],
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
})
