import winsound
import math
import re


durationNotes = {1:"WholeNote", 2:"HalfNote", 4:"QuarterNote", 8:"EightNote", 16:"SixteenthNote", 32:"ThirtyTwothNote"}
noteToFreqDitch = {
'C0':16.35,'C0Sharp':17.32,'D0':18.35,'D0Sharp':19.45,'E0':20.6,'F0':21.83,'F0Sharp':23.12,'G0':24.5,'G0Sharp':25.96,'A0':27.5,'A0Sharp':29.14,'B0':30.87,
'C1':32.7,'C1Sharp':34.65,'D1':36.71,'D1Sharp':38.89,'E1':41.2,'F1':43.65,'F1Sharp':46.25,'G1':49,'G1Sharp':51.91,'A1':55,'A1Sharp':58.27,'B1':61.74,
'C2':65.41,'C2Sharp':69.3,'D2':73.42,'D2Sharp':77.78,'E2':82.41,'F2':87.31,'F2Sharp':92.5,'G2':98,'G2Sharp':103.83,'A2':110,'A2Sharp':116.54,'B2':123.47,
'C3':130.81,'C3Sharp':138.59,'D3':146.83,'D3Sharp':155.56,'E3':164.81,'F3':174.61,'F3Sharp':185,'G3':196,'G3Sharp':207.65,'A3':220,'A3Sharp':233.08,'B3':246.94,
'C4':261.63,'C4Sharp':277.18,'D4':293.66,'D4Sharp':311.13,'E4':329.63,'F4':349.23,'F4Sharp':369.99,'G4':392,'G4Sharp':415.3,'A4':440,'A4Sharp':466.16,'B4':493.88,
'C5':523.25,'C5Sharp':554.37,'D5':587.33,'D5Sharp':622.25,'E5':659.25,'F5':698.46,'F5Sharp':739.99,'G5':783.99,'G5Sharp':830.61,'A5':880,'A5Sharp':932.33,'B5':987.77,
'C6':1046.5,'C6Sharp':1108.73,'D6':1174.66,'D6Sharp':1244.51,'E6':1318.51,'F6':1396.91,'F6Sharp':1479.98,'G6':1567.98,'G6Sharp':1661.22,'A6':1760,'A6Sharp':1864.66,'B6':1975.53,
'C7':2093,'C7Sharp':2217.46,'D7':2349.32,'D7Sharp':2489.02,'E7':2637.02,'F7':2793.83,'F7Sharp':2959.96,'G7':3135.96,'G7Sharp':3322.44,'A7':3520,'A7Sharp':3729.31,'B7':3951.07,
'C8':4186.01,'C8Sharp':4434.92,'D8':4698.63,'D8Sharp':4978.03,'E8':5274.04,'F8':5587.65,'F8Sharp':5919.91,'G8':6271.93,'G8Sharp':6644.88,'A8':7040,'A8Sharp':7458.62,'B8':7902.13
}
durationTimeNotes = {1:240.0, 2:120.0, 4:60.0, 8:30.0, 16:15.0, 32:7.5}


def main():
	inputstring = "\
2#a1 2f1 4- 8#a1 8c2 8d2 8#d2 2f2 2- 4f2 4f2 8#f2 8#g2 2#a2 2- 4#a2 8#a2 8- 8#g2 8#f2 4#g2 8#f2 2f2 2- 2f2 4#d2 8#d2 8f2 2#f2 2- 4f2 4#d2 4#c2 8#c2 8#d2 2f2 2- 4#d2 4#c2 4c2 8c2 8d2 2e2 2- 2g2 1f2"
	tempo = 200.0
	pitch_shift = 2
	naam = "zelda"
	playSound = True
	#parseSong(inputstring, tempo, naam, playSound, pitch_shift)
	
	f = open('s.txt', 'r')
	fout = open('s_out.txt', 'w')
	
	currentName = None
	currentTempo = None
	
	for line in f:
		#print(line)
		if line[0] == ' ' and line[1] == ' ':
			inputstring = line[2:].rstrip()
			print(repr(inputstring))
			#if '.' not in inputstring:
			parseSong(inputstring, currentTempo, currentName, playSound, pitch_shift)
						
		else:
			print(line)
			splitLine = line.split('Tempo=')
			currentTempo = int(splitLine[1].split(')')[0])
			regex = re.compile('[^a-zA-Z]')
			currentName = regex.sub('', splitLine[0])
			currentName = currentName[0].lower() + currentName[1:]
			print(currentName, currentTempo)
			
			
			

def parseSong(inputstring, tempo, naam, playSound, pitch_shift):
	totalDuration = 0
	current = 0

	methodString = "public static void " + naam + "(RoombaJSSC roomba)\n{\n"

	numberOfSongs = int(math.ceil(len(inputstring.split(' ')) / 16.0))
	#Print load songnames for the method
	for i in range(numberOfSongs):
		methodString += "	roomba.song("+str(i)+", " + naam + str(i+1) + ", " + str(int(tempo)) + ");\n"

	#Start printing notes
	for i, noteString in enumerate(inputstring.split(' ')):
		#Every 4 notes, add a new line for clarity
		if i % 4 == 0:
			print("")
		#Every 16 notes, create a new RoombaSongNote[]
		if i % 16 == 0:
			current += 1
			if current != 1:
				methodString += "	roomba.play("+str(current-2)+");\n"
				methodString += "	roomba.sleep(" + str(int(totalDuration*1000)+50) + ");\n"
				totalDuration = 0
				print("};\npublic static RoombaSongNote[] " + naam + str(current) + " = {")
			else:
				print("//"+naam+" songnotes")
				print("public static RoombaSongNote[] " + naam + str(current) + " = {")

		length = None
		note = None
		extended = False
		rest = None
		if noteString[0] == '1' and noteString[1] == '6':
			length = 16
			rest = noteString[2:]
		elif noteString[0] == '3' and noteString[1] == '2':
			length = 32
			rest = noteString[2:]
		else:
			length = int(noteString[0])
			rest = noteString[1:]
			
		if rest[0] == '.':
			extended = True
			rest = rest[1:]
			
		if rest[0] == '-':
			note = "Pause"
		elif rest[0] == '#':
			rest = rest[1:]
			note = rest.upper() + "Sharp"
		else:		
			note = rest.upper()
		
		totalDuration += durationTimeNotes[length] / tempo
			
		
		print("\tnew RoombaSongNote(RoombaNote."+note+", RoombaNoteDuration."+durationNotes[length]+"),")
		if playSound:
			ms = int((durationTimeNotes[length] / tempo) * 1000 )
			newNote = ""
			for c in note:
				if c.isdigit():
					newNote += str(int(c) + pitch_shift)
				else:
					newNote += c
			if note != 'Pause':
				winsound.Beep(int(noteToFreqDitch[newNote]), ms)
			else:
				from time import sleep
				sleep(ms / 1000.0)
	print("}\n")
	current += 1 
	methodString += "	roomba.play("+str(current-2)+");\n"
	methodString += "	roomba.sleep(" + str(int(totalDuration*1000)+50) + ");\n}"
	print(methodString)

if __name__ == "__main__":
    main()