import ctypes
import time
from agora.rtc.agora_service import ExternalVideoFrame, PcmAudioFrame

def prepare_frame_buffer(frame):
    """
    Prepares a frame buffer by concatenating YUV planes.
    """
    y_plane, u_plane, v_plane = frame.planes
    y_size = y_plane.height * y_plane.line_size
    u_size = u_plane.height * u_plane.line_size
    v_size = v_plane.height * v_plane.line_size

    frame_buf = bytearray(y_size + u_size + v_size)
    offset = 0
    for plane in frame.planes:
        ctypes.memmove(
            ctypes.addressof(ctypes.c_char.from_buffer(frame_buf, offset)),
            plane.buffer_ptr,
            plane.height * plane.line_size
        )
        offset += plane.height * plane.line_size

    return frame_buf

def create_external_video_frame(frame_buf, frame):
    """
    Creates an ExternalVideoFrame object for Agora.
    """
    return ExternalVideoFrame(
        buffer=frame_buf,
        type=1,  # Raw data
        format=1,  # YUV420
        stride=frame.width,
        height=frame.height,
        timestamp=int(time.time() * 1000)
    )

def prepare_audio_frame_buffer(frame):
    """
    Prepares an audio frame buffer from the input AudioFrame.
    """
    samples = frame.samples
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)
    # buffer_size = samples * channels * 2  # 16-bit PCM = 2 bytes per sample
    buffer_size = int(sample_rate*channels*0.1*2)
    audio_frame_buffer = bytearray(buffer_size)

    ctypes.memmove(
        ctypes.addressof(ctypes.c_char.from_buffer(audio_frame_buffer)),
        frame.planes[0].buffer_ptr,
        buffer_size
    )
    return audio_frame_buffer

def create_external_audio_frame(audio_frame_buf, frame):
    """
    Creates a PcmAudioFrame object for Agora.
    """
    return PcmAudioFrame(
        data=audio_frame_buf,
        timestamp=int(time.time() * 1000),  # Added timestamp
        samples_per_channel=frame.samples,
        bytes_per_sample=2,  # 16-bit audio
        number_of_channels=len(frame.layout.channels),
        sample_rate=frame.sample_rate
    )
