hello people,
Im Zaid here and this is one of my most exciting project. This project is an application named as EasyMeet, which is purely built from python and is completely offline.
This python application summarises the content of a recorded meeting video to give its users a quality summarized content without loosing any vital information.
Basically, this application divides the whole process into 4 simple steps/modules, namely:
                                     1)video processing
                                     2)audio processing
                                     3)sentence classification
                                     4)summarization(final part)

1) video processing: In this step, the video is processed ie, text is extracted from video by using pytesseract engine and open-cv.
                     the video is processed frame by frame, where the text is extracted from each frame.
                     an optimised way is used where similar frames are skipped based on frame numbers(divisible by threshold value) and differetiated based on pixel differences.
                     pytesseract is used to extract text from the selected frames and the text extracted is given to the sentence classifier(transformer) for filtering good and bad sentences.
                     another optimization is done where the text extracted in a text file is further preprocessed to remove duplicate texts in the text file("vtext.txt")

2)audio processing: In this step, the audio is extracted from the video in mp3 format using moviepy library and is converted to the respective wav file using ffmpeg engine as a subprocess in system.
                    Vosk library, that uses a speech to text model(separately downloaded) uses a kaldi recognizer, which is a wrapper function for the dowloaded model to convert the audio file(wav format) to text in json format.
                    The text is then written onto a text file named "atext.txt"

3)sentence classification: In this step, audio text file("atext.txt") is converted into csv file("atext.csv") and merged,shuffled with an already present random sentence csv file to produce a dataset that will be used for classification purpose.
                           The above dataset is then used for training a multinomial naive bayes classifier to classify whether a line in video text file is related to the information given by audio text file or not.
                           A final text file is then written with the text from audio text file and classified text from the video text file and saved as "text.txt", which will be summarized in the next step.

4)summarization: In this step, we use a summarization transformer called as distilbart, which summarizes the content/text in the main text file.
                 The text which might be huge is tokenized to reduce the words into their tokens and then separated into chunks of 1000 tokens as the transformer used can process only 1024 tokens.
                 Multiple chunks of tokens are then summarized in turns to print the final summary of the text extracted from both the video as well as audio.


IMPORTANT POINTS:
. This application is completely offline, even though it runs only once online to download the models(just once).
. Due to its offline capability, the confidential data shared in the office meetings can be safely processed with minimum risk
. This model runs a bit slow due to offline processing of the data and use of systems resources. If a system has good resources like cpu, ram, then this application summarizes quickly.
. The video processing and audio processing run in parallel with the help of threading technology used in the main python file.
. Proper usage of memory/space is done by removing the unnecessary files when not required

FUTURE ADD-ON'S:
. Error/Exception handling 
. Extracting the tasks that to be done and their timilines from the text and updating the calender with those extracted tasks

THIS APPLICATION CAN BE EXECUTED THROUGH THE "main.py" FILE. MAKE SURE U HAVE THE MODULES/LIBRARIES GIVEN IN THE REQUIREMENTS LIST!

FOLLOW UP FOR MORE AND MORE EXCITING UPDATES!
BOOYAH!!!!!!!!
