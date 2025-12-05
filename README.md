# Programming-for-Digital-Arts-Final-Project

Hoard Of Freaks
 
 A small game where you fend of the hoards of freaks that constantly come. each freak Has randomised stats and grow more powerfull
 as time goes on. you play as a turret that levels up by killing freaks. 



This project works off of 3 main classes Freak, Bullet, and Turret. using these classes the main function spawns freaks shoots bullets and creates a turret. the way that the freaks stats are desided is using a function called EnemyHealthSpeedGenerator. The function works by reciveing the current seconds survived and using that to increase the max amount of points a freak can have every 20 seconds. from there it choses a random number between 1 and the max points and flips a coin that may times. for each time the coin lands on health it gives that freak a point of health, and the same for speed. this system means that freaks are effectively choosing to invest in speed or health with their points

for every ten freaks killed your fire rate increases, and every 100 freaks gives you one more damage. Right now there is always a point where the freaks overrun you. I may make some balance changes. RIght now the game lasts about five min. I feel like that Is a good length for each run but I want to give It a little bit more feeling of skill. 


There are several things that I want to add. such as upgrades, like peircing bullets or multi shot. some other cool features that I would like to add would be giant freaks that are twice the size of the regular freaks that spawn rarely. I have also thought about addinng rare freaks that spawn 1 in 1000 just to add more interesting events, or to add little plants or rocks that spawn randomly around on the map just to add a visual detail. I also want to add more stat trackers and make a top score. 

in the assets fileyou will find all of the assets for the game.

Youtube video:
https://www.youtube.com/watch?v=tLoRmBADLA0

GitHub:
https://github.com/vaughnswanson/Programming-for-Digital-Arts-Final-Project

The final project for my Programming for Digital arts class









credits:



Python documentation:

https://docs.python.org/3/library/winsound.html

pygame documentation

https://www.pygame.org/docs/ref/math.html


stack overflow:

https://stackoverflow.com/questions/58940202/how-do-i-create-a-hitbox-for-all-shapes-in-my-program-and-a-way-to-detect-collis

https://stackoverflow.com/questions/6775897/pygame-making-a-sprite-face-the-mouse

https://stackoverflow.com/questions/307305/play-a-sound-with-python

https://stackoverflow.com/questions/43758189/how-to-stop-a-sound-that-is-playing-in-python

https://stackoverflow.com/questions/77748917/when-how-to-use-nonlocal


reddit:

https://www.reddit.com/r/learnpython/comments/rbs163/winsound_plays_error_sound_instead_of_the_file/

https://www.reddit.com/r/pygame/comments/18q5dns/how_should_game_states_be_handled/#:~:text=Game%20State%20Handling:%20Using%20a%20state%20machine,class%20with%20a%20draw%20and%20update%20function.%22

amudacodes blog:

https://amudacodes.hashnode.dev/mastering-game-flow-pygames-secret-sauce-for-seamless-state-transitions