#importing all the modules
from videoprocessing import *
from audioprocessing import *
from sentence_classification import *
from summarization import *
import threading

n=input("enter the name of video file without extension(it should be in same directory as that of this application):")


#threading for multitasking of both audio and video processing
t1=threading.Thread(target=vp,args=(n,)) #threading video processing module
t2=threading.Thread(target=ap,args=(f"{n}.mp4",)) #threading audio processing module

t1.start()
t2.start()

#making the main program wait until the two threads finish
t1.join()
print("video processing done!")
t2.join()
print("audio processing done!")

sc()
print("sentence classification done!")
summarize()
print("summarization done!")


#remving the unnecessary files after all the processing to save space
os.remove("atext.csv")
os.remove("atext.txt")
os.remove("vtext.txt")
os.remove("text.txt")

