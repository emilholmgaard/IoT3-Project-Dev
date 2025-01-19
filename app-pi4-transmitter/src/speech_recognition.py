import azure.cognitiveservices.speech as speechsdk
from gpiozero import LED

red_led = LED(19)

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(
        subscription="BLQyfL3cznQPolyd8jPmJLEkFaazRjqbPrgLHdOUBAg6iyzToVFLJQQJ99ALACi5YpzXJ3w3AAAYACOGJr9p",
        region="northeurope"
    )
    speech_config.speech_recognition_language = "da-DK"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    red_led.on()
    result = recognizer.recognize_once_async().get()
    red_led.off()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_speech = result.text
        return recognized_speech

    return None
