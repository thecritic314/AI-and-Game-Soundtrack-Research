# AI-and-Game-Soundtrack-Research

This repository contains my research project on the topic of Human Aware AI in Sound and Music.

## Abstract

In this paper, we present a novel technique for dynamically generating emotionally-directed video game soundtracks. Our approach involves a human Conductor who observes gameplay and directs associated emotions to enhance the gameplay experience. We employ supervised learning to train a mathematical model based on data collected from synchronized input gameplay features and Conductor output emotional direction features. During gameplay, the emotional direction model maps gameplay state input to emotional direction output, which is then used by a music generation module to dynamically create emotionally-relevant music. Our empirical study indicates that random forests are suitable for modeling the Conductor in our two experimental game genres.

## Open Source Games

The research focuses on two open source games: Bouncy Shots and Chaosman Overloaded. If you are interested in learning more about the techniques used, you can refer to the official paper titled "Learning Adaptive Game Soundtrack Control". Additionally, we have provided the base code, collected data, and the music engine implementation. To see the final products in action, you can run `bouncy_shots.py` and `chaosman.py` in the source folder. Please note that the models will need to process all the data again, so it may take some time.

## Credits

This research project was conducted under the guidance of Professor Todd Neller, with contributions from Aaron Dorsay and Veysel Yilmaz.
