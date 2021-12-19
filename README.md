# ME266K-Senior_Design-SwallowDectection - README

## UT Austin Fall 2021 Mechanical Engineering Senior Design Project:
### Evaluation of Optimal Sensor Locations for Swallowing Detection

#### Project Description:
Swallowing is an essential physiological function that all humans perform. It is used for absorbing nutrients during food/water consumption and even contributes to quality of life. Approximately 10 million people in the US suffer from dysphagia, or difficulty swallowing. Current methods for swallow detection - videofluoroscopy, endoscopy, monometry, etc. - are bulky, obtrusive, and uncomfortable; none of which can be performed outside a clinical setting.

For our project, we developed an experimental procedure and corresponding data analysis code to determine the optimal locations on the neck to put a knitted strain sensor for swallow detection.

#### Code Description:
I wrote a computer vision script that:
* uploads a swallowing/coughing/vocalizing video
* allows users to select markers on the neck to track
* calculates strain between all detected dots
* outputs top three sets of markers with highest strain
* produces heat map of neck that draws all locations of <10% strain

We wrote two versions of our code: one to be run locally and another to be run automatically on the Texas Advanced Computing Center (TACC). Both versions will be included in this repository.
