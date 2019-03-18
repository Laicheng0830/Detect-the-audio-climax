Audio detection climax part of music
1. method of use

1. If this is the result, change DIR_PATH = 'E:/Low_frequency_wav/' to its own file directory

The output result format is:

E:/Low_frequency_wav/$hinTo - OMG

Start times: (1, 50) (2, 10) # the corresponding time of the audio file climax (1, 50) represents the beginning of 1 minute 50 seconds, and 2 minutes 10 seconds is the corresponding relationship

Corr Max and id 0.1943366545709733 [11, 13] # the numerical value of the phase relationship is 0.19433 in the 11th and 13th frames is the climax, here is a 10-second sub-frame so the corresponding time is 11*10 is 1 min 50 seconds

(18, 18) # correlation coefficient matrix

2. Other code calls

The import audio_selector as ads

Let's get rid of the mute at the beginning

Data = ads.silence_detection(data) # returns the part of audio that starts with 0 filtered out

Call again to see which frame is at the top of the audio

Corr,id1,id2 = determine_audio(data,fs) # corr is the maximum 10-second correlation coefficient of all returned songs,id1 and id2 are 
the frames with the maximum correlation coefficient corresponding to the climax

2.Brief introduction to the principle

1. Generally speaking, the climax part of music will be repeated twice, based on which the following is done:

Frame the audio every 10 seconds

The correlation coefficient matrix is obtained by panywise correlation of the sub-frames

Find the correlation coefficient matrix to remove the maximum value of the diagonal phase relationship

For example: correlation coefficient matrix

I'm going to set all the data in the lower left hand corner to 1 because the lower left hand corner is the same as the upper right hand corner and I'm going to just look at the half, and the upper right hand corner is going to be the maximum value for each frame in relation to each other

Results 2.

After testing 671 songs, only 57% of the data could be paired with a correlation coefficient greater than 0.6.

The maximum correlation coefficient is 1, which can be set as greater than 0.6 to select this section of music

The music composition is different in style only 57% of the music can be found with two repeated passages
