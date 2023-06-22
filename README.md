# AI-and-Game-Soundtrack-Research


 This is my research project into the topic of Human Aware AI in Sound and Music.
 Abstract: In this paper, we demonstrate a novel technique for dynamically generating an emotionally-directed video game soundtrack. We begin with a human Conductor observing gameplay and directing associated emotions that would enhance the observed gameplay experience. We apply supervised learning to data sampled from synchronized input gameplay features and Conductor output emotional direction features in order to fit a mathematical model to the Conductor’s emotional direction. Then, during gameplay, the emotional direction model maps gameplay state input to emotional direction output, which is then input to a music generation module that dynamically generates emotionally-relevant music during gameplay. Our empirical study suggests that random forests serve well for modeling the Conductor for our two experimental game genres.
 The research focuses on 2 open source games: Bouncy Shots and Chaosman Overloaded. If you want to learn more about the techniques, you can take a look at the official paper "Learning Adaptive Game Soundtrack Control". In addition, I have included our base code and all the data that we collected and the music engine that we implemented. To check out our final products, you can try to run the bouncy_shots.py and the chaosman.py in the source folder. Notice that it may take some time because the models have to process all the data again.

Credits to Professor Todd Neller, Aaron Dorsay, and Veysel Yilmaz.
