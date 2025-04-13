from pydub import AudioSegment, silence

def analyze_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    duration_sec = len(audio) / 1000

    silent_chunks = silence.detect_silence(audio, min_silence_len=2000, silence_thresh=-40)
    dead_air_total = sum([end - start for start, end in silent_chunks]) / 1000

    # Fake data for now
    return {
        "total_duration_sec": duration_sec,
        "dead_air_sec": round(dead_air_total, 2),
        "dead_air_percent": round((dead_air_total / duration_sec) * 100, 2),
        "hold_time_sec": 5.0,  # Could be tracked from TwiML events
        "overtalk_events": 3   # Could be estimated with audio processing (advanced)
    }
