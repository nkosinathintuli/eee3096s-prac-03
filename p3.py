# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time
# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
#current=-1
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
#pwm_acc = None
eeprom = ES2EEPROMUtils.ES2EEPROM()
time_debounce = 0

# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    eeprom.populate_mock_scores()
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        global value
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    
    for j in range(3):
        score_info = raw_data[slice(j*4, j*4+4)]
        usrname = ''.join(score_info[slice(0,3)])
        c = j+1
        print(str(c)+" - "+usrname+" took "+str(score_info[3])+" guesses")
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_value[0], GPIO.OUT)
    GPIO.setup(LED_value[1], GPIO.OUT)
    GPIO.setup(LED_value[2], GPIO.OUT)
    GPIO.setup(LED_accuracy, GPIO.OUT)

    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setwarnings(False)

    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Setup PWM channels
    global pwm_acc
    pwm_acc=GPIO.PWM(LED_accuracy, 50)
    pwm_acc.start(0)

    global buzz
    buzz=GPIO.PWM(buzzer,1)
    buzz.start(0)
    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit,GPIO.FALLING,callback=btn_guess_pressed)
    GPIO.add_event_detect(btn_increase,GPIO.FALLING,callback=btn_increase_pressed,bouncetime=200)
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    score_count = eeprom.read_byte(0) # 1st 4 byte for no of scores stored
    scores = eeprom.read_block(1, score_count*4)
    # convert the codes back to ascii
    count = 0
    for i in range(len(scores)):
        count+=1
        if count == 4:
            count = 0
        else:
            scores[i] = chr(scores[i]) 
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    #global counter
    #counter1=time.time() 
    if (True):
       v1=0
       v2=0
       v3=0
       global current
       current=current+1
       if current==8:
          current=0
       print(current)
       GPIO.output(LED_value[2], GPIO.LOW)
       GPIO.output(LED_value[1], GPIO.LOW)
       GPIO.output(LED_value[0], GPIO.LOW)
       current1=current
    # Increase the value shown on the LEDs
       for i in range(3):
          if i==0:
             v1=current1%2
          if i==1:
             v2=current1%2
          if i==2:
             v3=current1%2
          current1=current1//2
    # You can choose to have a global variable store the user's current guess,
       if v3==1:
          GPIO.output(LED_value[1], GPIO.HIGH)
       if v2==1:
          GPIO.output(LED_value[2], GPIO.HIGH)
       if v1==1:
          GPIO.output(LED_value[0], GPIO.HIGH)

    # or just pull the value off the LEDs when a user makes a guess
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    global counter
    counter1=time.time()
    while GPIO.input(btn_submit)== GPIO.LOW:
       time.sleep(0.01)
    length=time.time()-counter1
    if (length)>=2:
       GPIO.cleanup()
       end_of_game=True
       length=0
    #counter=counter1
    if (counter1-counter)>=0.3:
       #GPIO.cleanup()
#      counter=counter1
       accuracy_leds()
    # if it's close enough, adjust the buzzer
       trigger_buzzer()
#       if value==current:
#          GPIO.cleanup()
#    if (counter1-counter)>=2:
#       GPIO.cleanup()
    #counter=counter1
       #counter=counter1
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%/
    acc=0.01
    if value<=current:
       acc=((8-current)/(8-value))*100
    else:
       acc=current/value*100
    pwm_acc.ChangeDutyCycle(acc)
    if value==current:
       pwm_acc.ChangeDutyCycle(0.01)
    
    print(value)
    print(current)
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    buzz.ChangeDutyCycle(50)
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    x=abs(current-value)
    if x==0:
       buzz.ChangeDutyCycle(0.01)
    if x==3:
       buzz.ChangeFrequency(1)
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    if x==2:
       buzz.ChangeFrequency(2)
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    if x==1:
       buzz.ChangeFrequency(4)
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        counter=time.time()
        setup()
        welcome()
        current=-1
        value=-1
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        pwm_acc.stop()
        buzz.stop()
