UPLOAD_TO = 'before_conversion'
SAVE_TO = 'after_conversion'

# for Music Model validator 
MAX_SIZE = 5*1024**2 # 10MB
ALLOWED_CONTENT_TYPES = (
    'audio/mpeg',                                              # .mp3
    'audio/wav', 'audio/wave', 'audio/x-wav', 'audio/x-pn-wav' # .wav
) 

# 参考: https://artists.spotify.com/help/article/loudness-normalization
TARGET_LOUDNESS = -14.0 # same as spotify, youtube 
