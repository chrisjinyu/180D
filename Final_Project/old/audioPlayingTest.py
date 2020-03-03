from playsound import playsound
WRONG_ANSWER = "files/buzzer.wav"
CORRECT_ANSWER = "files/clang.mp3"
GAME_WIN = "files/TaDa.mp3"

playsound(WRONG_ANSWER)
playsound(CORRECT_ANSWER)
for i in range(3):
	playsound(GAME_WIN)