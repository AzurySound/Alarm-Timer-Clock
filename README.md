# Alarm-Timer-Clock
## Welcome to ATC!

The product is aimed to be an effective widject for self time micromanagement.
There is a packed exe file available to download and run.

The code is distributed between 3 .py files:
### Main.py
At that stage Main.py could use refactoring and should be splitted into separated classes removing a bunch of global variables and increasing readability. I used the following frameworks there: tkinter and time, calculation methods and functions from WIndowsTimer.py file to showcase the accurate clock view.
### WindowsTimer.py
WindowsTimer.py uses time framework and an original ClockHand class which provides the logic to calculate the desired time in different modes.
### ClockHand.py
ClockHand class is designed for time calculations within an OOP approach.





---------------------------
## Options
After start the clock is shown. It is draggable and can be set as an Alarm, Timer and Stopwatch that shows only minutes and hours. 
There are few options in the dropdown menu:
1. User can choose the size of the clock **smaller/bigger**
2. **The color** of the digits can be changed with a double click on them 
3. **The font** of the digits can be changed by picking the Font option in the dropdown menu
4. User can change whether to show the clock **on top** of the desktop or **off top** (by default bigger size is off and smaller size is on)
5. User can change the **transparency** with a middle mouse click on the clock
6. In the settings menu **a note** can be added to the clock
7. User can switch back to **the clock view any time** with the clock option in the dropdown menu. (it's a shortcut to avoid opening settings window)
To set up an Alarm, Timer and Stopwatch
there's a settings menu available in the dropdown menu:
---------------------------

## Settings menu:

There is a short hint on what are Alarm, Timer and Stopwatch for:
Alarm counts down to the exact time that has been put in the input fields
Timer counts down an exact time that has been put in the input fields
Stopwatch is activated by a Timer button if all the fields left empty or fulfilled with zeros

There are 3 input fields:
Hours   Minutes   Seconds

There are 3 buttons that activate a relative mode:
Clock   Alarm   Timer

When a mode is active it cannot be activated again until switched to another mode.

There's a 4th input field for your comment located at the bottom of ATC window.
The commend is shown the next second you start typing in the field.

---------------------------

I wish you enjoy the ATC app and manage your time wisely! 
