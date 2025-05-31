import speech_recognition as sr
import difflib
import string

def normalize_text(text):
    # Lowercase and remove punctuation
    return ''.join([c.lower() for c in text if c not in string.punctuation])

def get_speech_input(prompt="Please say something..."):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print(prompt)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return ""

def calculate_similarity(text1, text2):
    # Tokenize into words and compare sequences
    words1 = normalize_text(text1).split()
    words2 = normalize_text(text2).split()
    matcher = difflib.SequenceMatcher(None, words1, words2)
    return matcher.ratio() * 100  # As a percentage

if __name__ == "__main__":
    # This is the reference text; change as needed
    reference_text = "Hello, this is a sample statement for testing speech recognition accuracy."

    print("Reference phrase to match:")
    print(reference_text)
    print("\nSpeak into your microphone to test.")

    spoken_text = get_speech_input()

    print("\nYou said:")
    print(spoken_text)

    similarity = calculate_similarity(spoken_text, reference_text)
    print(f"\nMatch Percentage: {similarity:.2f}%")