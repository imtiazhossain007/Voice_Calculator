import speech_recognition as sr
import pyttsx3
import re
import sys
import math

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_voice_input():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Didn't catch that.")
        except sr.RequestError:
            print("❌ Speech service error.")
    return None

def words_to_number(text):
    num_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
        "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
        "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
        "eighty": "80", "ninety": "90"
    }

    for word, digit in num_words.items():
        text = re.sub(rf"\b{word}\b", digit, text)

    text = re.sub(r"(\d+)\s+point\s+(\d+)", r"\1.\2", text)
    return text

def parse_input(text, previous_result):
    text = words_to_number(text)

    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("into", "*")
    text = text.replace("divided by", "/")
    text = text.replace("over", "/")

    if "previous result" in text:
        text = text.replace("previous result", str(previous_result))

    sqrt_matches = re.findall(r"square root(?: of)? (\d*\.?\d+)", text)
    for match in sqrt_matches:
        number = float(match)
        sqrt_val = round(math.sqrt(number), 4)
        text = text.replace(f"square root of {match}", str(sqrt_val))
        text = text.replace(f"square root {match}", str(sqrt_val))

    raw_tokens = re.findall(r"[-+]?\d*\.?\d+|[+\-*/]", text)
    return raw_tokens

def evaluate_expression(tokens):
    expression = " ".join(tokens)
    try:
        result = eval(expression)
        if '/' in expression:
            result = round(result, 2)
        if '+' in expression:
            result = round(result, 2)
        return expression, result
    except Exception as e:
        print(f"❌ Evaluation error: {e}")
        return None, None

def voice_calculator():
    print("🔐 Say the password to start...")
    while True:
        command = get_voice_input()
        if command and "start buddy" in command:
            break

    speak("Identity Confirmed. hello sir")

    previous_result = 0

    while True:
        expression_tokens = []
        speak("Say your expression. Say 'equals' to evaluate.")

        while True:
            user_input = get_voice_input()
            if user_input is None:
                continue

            if "that's it buddy" in user_input:
                speak("Goodbye.")
                print("🛑 Program terminated by user.")
                sys.exit()

            if "delete" in user_input:
                if expression_tokens:
                    removed = expression_tokens.pop()
                    speak(f"Deleted {removed}")
                    print(f"🗑️ Deleted: {removed}")
                continue

            if "equals" in user_input or "equal" in user_input:
                expression, result = evaluate_expression(expression_tokens)
                if result is not None:
                    print(f"✅ Expression: {expression}")
                    print(f"🧮 Result: {result}")
                    speak(f"The result is {result}")
                    previous_result = result
                else:
                    speak("Sorry, I couldn't evaluate that.")
                break

            tokens = parse_input(user_input, previous_result)
            valid_tokens = [t for t in tokens if re.match(r'^[-+]?\d*\.?\d+$|^[+\-*/]$', t)]

            if valid_tokens:
                expression_tokens.extend(valid_tokens)
            else:
                print("⚠️ Ignored non-math content.")
                speak("Ignored that input.")

# Run the calculator
if __name__ == "__main__":
    speak("Welcome . Please confirm your identity")
    voice_calculator()


