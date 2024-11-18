from .agora_service import initialize_agora_service, setup_agora_connection, set_video_encoder_configuration
from .frame_handler import prepare_frame_buffer, create_external_video_frame, prepare_audio_frame_buffer, create_external_audio_frame
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
import asyncio
from storage import peer_connections

def setup_peer_connection():
    """
    Configures and returns the RTCPeerConnection object.
    """
    configuration = RTCConfiguration([
        RTCIceServer(urls="stun:128-14-195-194.edge.agora.io:443"),
        RTCIceServer(urls="stun:stun.l.google.com:19302"),
        RTCIceServer(urls="stun:stun1.l.google.com:19302"),
    ])
    return RTCPeerConnection(configuration)


async def handle_webrtc_connection(sdp_offer, resource_id, channel_id, uid):
    """
    Orchestrates Agora and WebRTC setup for the /whip endpoint.
    """

    agora_service = initialize_agora_service()
    connection, video_sender, audio_sender, video_track = await setup_agora_connection(agora_service, channel_id, uid)
    pc = setup_peer_connection()

    @pc.on("track")
    async def on_track(track):
        video_first_frame = True;
        if track.kind == "video":
            while True:
                try:
                    rcv_video_frame = await track.recv()
                    if video_first_frame:
                        set_video_encoder_configuration(video_track, width = rcv_video_frame.width, height = rcv_video_frame.height, frame_rate = 30)
                        video_first_frame = False
                    video_frame_buf = prepare_frame_buffer(rcv_video_frame)
                    video_frame = create_external_video_frame(video_frame_buf, rcv_video_frame)
                    ret = video_sender.send_video_frame(video_frame)
                    if ret < 0:
                        print(f"Failed to send video frame: {ret}")
                except Exception as e:
                    print(f"Error processing video track: {e}")
                    break
        elif track.kind == "audio":
            while True:
                try:
                    rcv_audio_frame = await track.recv()
                    audio_frame_buf = prepare_audio_frame_buffer(rcv_audio_frame)
                    audio_frame = create_external_audio_frame(audio_frame_buf, rcv_audio_frame)
                    audio_sender.send_audio_pcm_data(audio_frame)
                except Exception as e:
                    print(f"Error processing audio track: {e}")
                    break


    sdp_answer = await finalize_sdp_exchange(pc, sdp_offer)
    peer_connections[resource_id] = pc
    return sdp_answer

async def finalize_sdp_exchange(pc, sdp_offer):
    """
    Completes the SDP exchange and returns the SDP answer.
    """
    await pc.setRemoteDescription(RTCSessionDescription(sdp_offer, "offer"))
    print("Remote SDP offer set.")

    await pc.setLocalDescription(await pc.createAnswer())
    print("Local SDP description set.")

    while pc.iceGatheringState != "complete":
        await asyncio.sleep(0.1)
    print("ICE gathering complete.")

    return pc.localDescription

async def cleanup_connection(pc, resource_id):
    """
    Cleans up resources for the specified connection.
    """
    if resource_id in peer_connections:
        del peer_connections[resource_id]
    await pc.close()
    print(f"Cleaned up connection {resource_id}")
