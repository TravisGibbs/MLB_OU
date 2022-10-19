# MLB_OU
Hi this is the source code for a website hosted on Python Anywhere [here](http://travismlb.pythonanywhere.com/)

I did web scraping to find all player data, card images, and lots of hard hit ball videos from baseball reference, baseball savant, and baseball alamanc.
I used audio proccessing to extract feature maximums to find momenets where the ball is hit in any given baseball hit. For now the time is determined by a simple analysis of energy entropy.
From there I built a basic flask app to allow the user to play two different games one that is a sort of higher lower and one is asking the user to do a prediction given the start of a video.


![image](https://user-images.githubusercontent.com/28307522/196770289-6552f654-45ac-4f02-a1ac-329d24737522.png)
