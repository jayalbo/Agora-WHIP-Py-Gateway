import os
from config import APP_ID, CERTIFICATE
from libs.token_generator.RtcTokenBuilder2 import RtcTokenBuilder
from agora.rtc.agora_service import AgoraService, RTCConnection, VideoEncoderConfiguration, VideoDimensions, AgoraServiceConfig
from agora.rtc.agora_base import ClientRoleType, RTCConnConfig, ChannelProfileType, AudioScenarioType
from storage import agora_peer_connections

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def initialize_agora_service():
    """
    Initializes the AgoraService with logging configuration.
    """
    agora_service = AgoraService()
    config = AgoraServiceConfig(appid=APP_ID, enable_video=1)
    agora_service.initialize(config)


    agora_service.set_log_file(os.path.join(LOG_DIR, "agorasdk.log"))
    print(f"Agora logs will be saved to {LOG_DIR}")
    return agora_service
def set_video_encoder_configuration(video_track, width, height, frame_rate = 30):
    """
    Sets the video encoder configuration for the video track.
    """
    video_config = VideoEncoderConfiguration(
        frame_rate=frame_rate,
        dimensions=VideoDimensions(width=width, height=height),
        encode_alpha=0
    )
    video_track.set_video_encoder_configuration(video_config)
async def setup_agora_connection(agora_service, channel_id, uid, resource_id):
    """
    Sets up the Agora connection and returns the connection object and video track.
    """
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)
    if not connection:
        raise Exception("Failed to create Agora connection")

    # Check if Certificate is set
    if CERTIFICATE:
        token = RtcTokenBuilder.build_token_with_uid(APP_ID, CERTIFICATE, channel_id, str(uid), 86400, 0)
    else:
        token = ""
    print(token)
    ret = connection.connect(token, channel_id, str(uid))
    if ret < 0:
        raise Exception(f"Failed to connect to Agora: {ret}")
    print("Connected to Agora successfully")
    agora_peer_connections[resource_id] = connection

    media_node_factory = agora_service.create_media_node_factory()

    # Set up Agora video track
    video_sender = media_node_factory.create_video_frame_sender()
    video_track = agora_service.create_custom_video_track_frame(video_sender)

    # Set up Agora audio track
    audio_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(audio_sender)

    # video_config = VideoEncoderConfiguration(
    #     frame_rate=30,  # Hardcoded FPS
    #     dimensions=VideoDimensions(width=1280, height=720),  # Default resolution
    #     encode_alpha=0
    # )
    # video_track.set_video_encoder_configuration(video_config)
    video_track.set_enabled(1)
    audio_track.set_enabled(1)

    local_user = connection.get_local_user()
    local_user.set_user_role(ClientRoleType.CLIENT_ROLE_BROADCASTER)
    local_user.publish_video(video_track)
    local_user.publish_audio(audio_track)
    print("Published video to Agora successfully")
    return connection, video_sender, audio_sender, video_track

async def cleanup_agora_connection(resource_id):
    """
    Cleans up the Agora connection and resources.
    """
    connection = agora_peer_connections.get(resource_id)
    if connection:
        connection.disconnect()
        connection.release()
        agora_peer_connections.pop(resource_id)
    print("Disconnected from Agora")
