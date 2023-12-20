# EyeTracker-Processing
Data Processing Code for Mobile Application (EyeTracker, BVG Software group LLC, the Netherlands)

Binocular eye movements, including saccades and smooth pursuits, were continuously recorded at a frequency of 20 Hz using a mobile eye-tracking system (EyeTracker, BVG Software Group LLC, the Netherlands). This system utilized visual cues displayed on a tablet screen. To ensure optimal conditions for eye-tracking, room lights and electronic devices were turned off during the follow-up sessions.

The protocol initiated with a calibration phase, where the tablet screen remained black for 10 seconds, allowing participants to adjust their vision. Subsequently, a circular marker with a 0.3 cm diameter appeared on the screen for 20 seconds. This marker moved randomly across the screen at varying speeds to facilitate the tracking of both saccades and smooth pursuits. To maintain participant attention on the marker's center, its color alternated between white and red every 2 seconds.

Frames of low quality, such as those with unrecognized pupils, incorrect initial frames, and blinking frames, were manually excluded using the network refinement function of the software. A sequence of the 300 best consecutive eye-tracking frames was analyzed prior to turning off the tablet screen. The entire procedure lasted for 30 seconds.

The parameters calculated from this data included vertical and horizontal angular velocity (AV), left vertical speed (LVS), right vertical speed (RVS), left horizontal speed (LHS), and right horizontal speed (RHS). Additionally, indices of vertical and horizontal eye version (version index, Vx) were computed. These were determined as the Pearson correlation coefficient between the corresponding AVs of the right and left eyes.
