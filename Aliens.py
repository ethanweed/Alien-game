# original script by Kristian Tylén

# See tak description in:
# Tylén, K., Fusaroli, R., Østergaard, S. M., Smith, P., & Arnoldi, J. (2023). 
# The Social Route to Abstraction: Interaction and Diversity Enhance Performance and Transfer in a 
# Rule‐Based Categorization Task. Cognitive Science, 47(9), e13338.

# script adapted 2015 by Ethan Weed
# script updated 2024-08-09 by Ethan Weed

# import modules
from psychopy import visual, core, event, gui # type: ignore
#prefs.general['audioLib'] = ['pygame']
from psychopy.sound import Sound
import pandas as pd
import glob
import random
import datetime

# get current date and time for naming logfiles
now = datetime.datetime.now()
print ("Current date and time : ")
t = now.strftime("%Y-%m-%d_%H%M%S")


# gui requesting participant info
participant_id = gui.Dlg(title='The Alien Game') 
participant_id.addText('Experiment Info')
participant_id.addField('pair', label='* Pair Number')
participant_id.addField('numTrials', label = '* Number of trials (2 - 96)')
participant_id.addField('level', choices = ['easy', 'medium', 'hard'])

#if pilot is chosen, no data will be saved to final .txt file
participant_id.addField('testPilot', choices = ['test', 'pilot']) 
ID = participant_id.show()


# define window
win = visual.Window(fullscr=True, color = '#f2e9e0') 

# define clock
exp_time = core.Clock()

# create a list of stimulus file names from a folder 
stimulus = glob.glob('pictures/[0-1]*.png')

STIMULUS = []


for i in range(3):
	random.shuffle(stimulus)
	STIMULUS = STIMULUS + stimulus
print(f"ID: {ID}")
TRIAL = int(ID['numTrials'])

# time 
EXP_TIME = 20000

# how long to show monster
# how long to wait before allowing participant to press space and continue
EXPOSURE_TIME = 4

if ID['level'] == 'easy':
         level_idx = -7
elif ID['level'] == 'medium':
         level_idx = -6
elif ID['level'] == 'hard':
         level_idx = -5

# load frames for final animation
FLICKER_FREQ = 0.2

num_frames = len(glob.glob('Rocket_frames/*.jpg'))

f_prefix = 'Rocket_frames/'
frame_names = []
for i in range(0, num_frames, 1):
     filename = f_prefix + str(i) + '.jpg' 
     frame_names.append(filename)



FRAMES = []
for i in range(0, len(frame_names), 1):
	frame = visual.ImageStim(win, image = frame_names[i], size = [2, 1.6])
	FRAMES.append(frame)
         
# buttons
IGNORE = visual.ImageStim(win, image = 'buttons/wave.png', pos = [-0.6, 0.0])
TAP = visual.ImageStim(win, image = 'buttons/ask.png', pos = [-0.2, 0.0])
KILL = visual.ImageStim(win, image = 'buttons/run.png', pos = [0.2, 0.0])
TAPKILL = visual.ImageStim(win, image = 'buttons/steal.png', pos = [0.6, 0.0])

SUCCESS = visual.ImageStim(win, image = 'pictures/success.png')
FAILURE = visual.ImageStim(win, image = 'pictures/failure.png')

# Intro
INSTRUCTIONS1 = visual.ImageStim(win, image = 'pictures/Instruction1.png', size = [1.8, 1.8])
INSTRUCTIONS2 = visual.ImageStim(win, image = 'pictures/Instruction2.png', size = [1.8, 1.8])
INSTRUCTIONS3 = visual.ImageStim(win, image = 'pictures/Instruction3.png', size = [1.8, 1.8])
INSTRUCTIONS4 = visual.ImageStim(win, image = 'pictures/Instruction4.png', size = [1.8, 1.8])

# Sounds
CHIME = Sound(value = "sounds/chime.wav")
TADA = Sound(value = "sounds/TaDa.wav")
WAWA = Sound(value = "sounds/SadTrombone_short.wav")

FEEDBACK_i = 'Oops! You should have just waved to this friendly alien.'
FEEDBACK_t = 'Oops! You should have asked this friendly alien for a gem.'
FEEDBACK_k = 'Oops! You should have run away from this bad alien.' 
FEEDBACK_x = 'Oops! You should have stolen a gem from this bad alien.' 

feedback_i = visual.TextStim(win, text = FEEDBACK_i, pos = [0, -0.4], color = 'black', height = 0.06)
feedback_t = visual.TextStim(win, text = FEEDBACK_t, pos = [0, -0.4], color = 'black', height = 0.06)
feedback_k = visual.TextStim(win, text = FEEDBACK_k, pos = [0, -0.4], color = 'black', height = 0.06)
feedback_x = visual.TextStim(win, text = FEEDBACK_x, pos = [0, -0.4], color = 'black', height = 0.06)

INS1 = visual.TextStim(win, text = '''
For every alien you see, talk together and decide whether to WAVE and move on, ASK for a gem, RUN away, or STEAL a gem. 

Wait for the chime before giving your answer.

You will earn 10 points for every correct choice, and lose 2 points for every mistake.
''', color = 'black', height = 0.06)

INS2 = visual.TextStim(win, text = '''
When you have looked at an alien and reached a decision, press the spacebar to see the decision buttons.

Click on the WAVE, ASK, RUN, or STEAL button to make your choice.
''', color = 'black', height = 0.06)

INS3 = visual.TextStim(win, text = '''
Good luck, and remember to make your choices together!
''', color = 'black', height = 0.06)

POINTS = 0

# define mouse
myMouse = event.Mouse()

# define clock
stopwatch = core.Clock()

# instruction
INSTRUCTIONS1.draw()
win.flip()
event.waitKeys()
INSTRUCTIONS2.draw()
win.flip()
event.waitKeys()
INSTRUCTIONS3.draw()
win.flip()
event.waitKeys()
INSTRUCTIONS4.draw()
win.flip()
event.waitKeys()

INS1.draw()
win.flip()
event.waitKeys()
INS2.draw()
win.flip()
event.waitKeys()
INS3.draw()
win.flip()
event.waitKeys()

# define a list "rows" to hold response data
rows = []

exp_time.reset()


for i in range(TRIAL):	
	stim = visual.ImageStim(win, image = STIMULUS[i], size = [2, 1.6])
	stim.draw()
	win.flip()
	core.wait(EXPOSURE_TIME)
	Sound.play(CHIME)


	keys = event.waitKeys()
	if "escape" in keys:
		break

	stopwatch.reset()
	endTrial = False
	while not endTrial:
		IGNORE.draw(); TAP.draw(); KILL.draw(), TAPKILL.draw()
		# get mouse button presses
		mouse1, mouse2, mouse3 = myMouse.getPressed()
		win.flip()
		# if mouse click - get position/image               
		if myMouse.isPressedIn(IGNORE):
			choice = 'wave'
			#choice = 'ignore'
			reaction_time = stopwatch.getTime()
			endTrial = True
			if STIMULUS[i][level_idx] == 'i':
				correct = 1
			else:
				correct = 0

		elif myMouse.isPressedIn(TAP):
			choice = 'ask'
			#choice = 'tap'
			reaction_time = stopwatch.getTime()
			endTrial = True
			if STIMULUS[i][level_idx] == 't':
				correct = 1
			else:
				correct = 0

		elif myMouse.isPressedIn(KILL):
			choice = 'run'
			#choice = 'kill'
			reaction_time = stopwatch.getTime()
			endTrial = True
			if STIMULUS[i][level_idx] == 'k':
				correct = 1
			else:
				correct = 0
  
		elif myMouse.isPressedIn(TAPKILL):
			choice = 'steal'
			#choice = 'tapandkill'
			reaction_time = stopwatch.getTime()
			endTrial = True
			if STIMULUS[i][level_idx] == 'x':
				correct = 1
			else:
				correct = 0

	if correct == 1:
		POINTS = POINTS + 10
		feedback = visual.TextStim(win, text = 'You made the right choice! You now have ' + str(POINTS) + ' points.\n\n\n (' + str(i+1) + '/' + str(TRIAL) + ' Aliens)', pos = [0, -0.5], color = 'black', height = 0.06)
		feedback.draw()
		SUCCESS.draw()
		Sound.play(TADA)

	else:

		POINTS = POINTS - 2
		if POINTS < 0:
			POINTS = 0
		else:
			POINTS = POINTS
		FAILURE.draw()
		Sound.play(WAWA)
		feedback = visual.TextStim(win, text = '\n\n\nYou made a mistake! You now have ' + str(POINTS) + ' points.\n\n (' + str(i+1) + '/' + str(TRIAL) + ' Aliens)', pos = [0, -0.5], color = 'black', height = 0.06)
		feedback.draw()
		if STIMULUS[i][level_idx] == 'i':
			feedback_i.draw()
		elif STIMULUS[i][level_idx] == 't':
			feedback_t.draw()
		elif STIMULUS[i][level_idx] == 'k':
			feedback_k.draw()
		elif STIMULUS[i][level_idx] == 'x':
			feedback_x.draw()



	win.flip()
	# time to show pos / neg feedback
	#core.wait(5)
	keys = event.waitKeys()


	rows.append([ID['pair'], i+1, STIMULUS[i][9:], choice, correct, POINTS, reaction_time])



	if "escape" in keys:
		break
	
	
	# if experiment runs for longer than EXP_TIME end the experiment
	#if exp_time.getTime() > EXP_TIME:
		#break

DONE_WIN = visual.TextStim(win, text = '''
The game is now done.

Together, you earned ''' + str(POINTS) + ' points.'

'That\'s enough gems to get your ship flying again!''', color = 'black', height = 0.06)

DONE_FAIL = visual.TextStim(win, text = '''
The game is now done.

Together, you earned ''' + str(POINTS) + ' points.'

'That\'s not enough gems to get your ship flying again!''', color = 'black', height = 0.06)


        
if POINTS > 0:
	DONE_WIN.draw()
	win.flip()
	event.waitKeys()
	win.flip()
	for frame in FRAMES:
		frame.draw()
		#core.wait(FLICKER_FREQ)
		win.flip()
	

	
	
else:
	DONE_FAIL.draw()
	win.flip()
	event.waitKeys()
	
DATA = pd.DataFrame(rows)
DATA.columns = ['ID', 'trial', 'image', 'choice', 'correct', 'point', 'reaction_time']

if ID['testPilot'] == 'test':
	DATA.to_csv('logfiles/logfile_' + t + '.csv', index = False)

