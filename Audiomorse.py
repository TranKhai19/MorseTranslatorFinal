import pyaudio
import wave
import MorseTranslator

def listen_morse_audio(audio_filename):
    # Load Morse audio
    wf = wave.open(audio_filename, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    print("Listening to Morse audio...")

    # Read data and play audio
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Stop stream and close PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__=="__main__":
    audio_filename = "./test.mp3"  # Path to your Morse audio file
    listen_morse_audio(audio_filename)
    morse_code = "... --- ..."
    print("Morse code:", morse_code)
