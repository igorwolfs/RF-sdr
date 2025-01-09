# Todo
- Figure out why the sending and receiving isn't aligned
- Do the necessary calibrations / adaptations to make sure they are aligned
- Try increasing the bandwidth, measuring and saving on the pluto, and then getting it from the pluto: https://ez.analog.com/adieducation/university-program/f/q-a/571424/adalm-pluto-fill-up-buffer-using-the-maximum-sampling-rate-and-read-it-after

- Recalibrate the pluto-frequency with satellite data: https://community.libre.space/t/correcting-frequency-offset-on-adalm-plutosdr/10717/3

# Steps from course
https://www.youtube.com/watch?v=EHQcuFuQA5w&t=182s&ab_channel=HarveyMuddPhysicsElectronicsLab
## Step 1:
Check difference in frequency spectrum, if everything is perfectly matched there should be a peak at 0.
If the peak isn't at 0, we must make sure to shift the peak so the frequency peak ends up being at 0.
