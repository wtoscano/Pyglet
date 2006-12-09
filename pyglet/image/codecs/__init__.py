#!/usr/bin/env python

'''Collection of image encoders and decoders.

Modules must subclass ImageDecoder and ImageEncoder for each method of
decoding/encoding they support.

Modules must also implement the two functions::
    
    def get_decoders():
        # Return a list of ImageDecoder instances or []
        return []

    def get_encoders():
        # Return a list of ImageEncoder instances or []
        return []
    
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import os.path

_decoders = []              # List of registered ImageDecoders
_decoder_extensions = {}    # Map str -> list of matching ImageDecoders
_encoders = []              # List of registered ImageEncoders
_encoder_extensions = {}    # Map str -> list of matching ImageEncoders

class ImageDecodeException(Exception):
    pass

class ImageEncodeException(Exception):
    pass

class ImageDecoder(object):
    def get_file_extensions(self):
        '''Return a list of accepted file extensions, e.g. ['.png', '.bmp']
        Lower-case only.
        '''
        return []

    def decode(self, file, filename):
        '''Decode the given file object and return an instance of Image.
        Throws ImageDecodeException if there is an error.  filename
        can be a file type hint.
        '''
        raise NotImplementedError()

class ImageEncoder(object):
    def get_file_extensions(self):
        '''Return a list of accepted file extensions, e.g. ['.png', '.bmp']
        Lower-case only.
        '''
        return []

    def encode(self, image, file, filename, options={}):
        '''Encode the given image to the given file.  filename
        provides a hint to the file format desired.  options are
        encoder-specific, and unknown options should be ignored or
        issue warnings.
        '''
        raise NotImplementedError()

def get_encoders(filename=None):
    '''Get an ordered list of encoders to attempt.  filename can be used
    as a hint for the filetype.
    '''
    encoders = []
    if filename:
        extension = os.path.splitext(filename)[1].lower()
        encoders += _encoder_extensions.get(extension, [])
    encoders += [e for e in _encoders if e not in encoders]
    return encoders

def get_decoders(filename=None):
    '''Get an ordered list of decoders to attempt.  filename can be used
     as a hint for the filetype.
    '''
    decoders = []
    if filename:
        extension = os.path.splitext(filename)[1].lower()
        decoders += _decoder_extensions.get(extension, [])
    decoders += [e for e in _decoders if e not in decoders]
    return decoders

def add_decoders(module):
    '''Add a decoder module.  The module must define `get_decoders`.  Once
    added, the appropriate decoders defined in the codec will be returned by
    pyglet.image.codecs.get_decoders.
    '''
    for decoder in module.get_decoders():
        _decoders.append(decoder)
        for extension in decoder.get_file_extensions():
            if extension not in _decoder_extensions:
                _decoder_extensions[extension] = []
            _decoder_extensions[extension].append(decoder)

def add_encoders(module):
    '''Add an encoder module.  The module must define `get_encoders`.  Once
    added, the appropriate encoders defined in the codec will be returned by
    pyglet.image.codecs.get_encoders.
    '''
    for encoder in module.get_encoders():
        _encoders.append(encoder)
        for extension in encoder.get_file_extensions():
            if extension not in _encoder_extensions:
                _encoder_extensions[extension] = []
            _encoder_extensions[extension].append(encoder)

# these functions are used to support unit testing turning off stuff
def get_encoders_state():
    return _encoders, _encoder_extensions
def get_decoders_state():
    return _decoders, _decoder_extensions
def set_encoders_state(state):
    global _encoders, _encoder_extensions
    _encoders, _encoder_extensions = state
def set_decoders_state(state):
    global _decoders, _decoder_extensions
    _decoders, _decoder_extensions = state
def clear_decoders():
    global _decoders, _decoder_extensions
    _decoders = []
    _decoder_extensions = {}
def clear_encoders():
    global _encoders, _encoder_extensions
    _encoders = []
    _encoder_extensions = {}

 
def add_default_image_codecs():
    # Add the codecs we know about.  These should be listed in order of
    # preference.  This is called automatically by pyglet.image.

    # Compressed texture in DDS format
    try:
        from pyglet.image.codecs import dds
        add_encoders(dds)
        add_decoders(dds)
    except ImportError:
        pass

    # Mac OS X default: QuickTime
    try:
        import pyglet.image.codecs.quicktime
        add_encoders(quicktime)
        add_decoders(quicktime)
    except ImportError:
        pass

    # Windows XP default: GDI+
    try:
        import pyglet.image.codecs.gdiplus
        add_encoders(gdiplus)
        add_decoders(gdiplus)
    except ImportError:
        pass

    # Linux default: GdkPixbuf 2.0
    try:
        import pyglet.image.codecs.gdkpixbuf2
        add_encoders(gdkpixbuf2)
        add_decoders(gdkpixbuf2)
    except ImportError:
        pass

    # Fallback: PIL
    try:
        import pyglet.image.codecs.pil
        add_encoders(pil)
        add_decoders(pil)
    except ImportError:
        pass

    # Fallback: PNG loader (slow)
    try:
        import pyglet.image.codecs.png
        add_encoders(png)
        add_decoders(png)
    except ImportError:
        pass

