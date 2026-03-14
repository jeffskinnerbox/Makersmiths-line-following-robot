# History and Application: Reinforcement Learning

**Subject:** Reinforcement learning — a branch of artificial intelligence where software agents learn to make decisions by interacting with an environment and receiving rewards or penalties
**Target Audience:** High school students in a robotics workshop
**Date:** 2026-02-19

## 1. History

### Brief History

Reinforcement learning grew out of a deceptively simple question: how do animals — and eventually machines — learn to do the right thing through trial and error? The story begins not with computers, but with cats. In 1898, psychologist [Edward Thorndike][01] placed hungry cats inside wooden "puzzle boxes" and timed how long it took them to escape and reach food. He noticed that actions leading to a satisfying result were repeated more often, a principle he called the [Law of Effect][02]. This idea — that behavior is shaped by its consequences — became the psychological foundation that reinforcement learning would eventually formalize in mathematics and code.

For decades the idea stayed in psychology. B.F. Skinner extended Thorndike's work in the 1930s-40s with [operant conditioning][03], training pigeons and rats using rewards and punishments. Meanwhile, mathematician [Richard Bellman][04] developed dynamic programming in the 1950s, creating equations for making optimal sequences of decisions — a completely separate thread that would prove essential later. These two threads — learning from consequences (psychology) and optimal decision-making (mathematics) — ran in parallel for years.

The threads converged in the 1980s when [Andrew Barto and Richard Sutton][05], working at the University of Massachusetts Amherst, began formalizing trial-and-error learning as a computational problem. Sutton introduced [temporal difference learning][06] in 1988, and Chris Watkins developed [Q-learning][07] in 1989, giving the field its core algorithms. Their 1998 textbook, *Reinforcement Learning: An Introduction*, became the field's bible. The deep learning revolution of the 2010s supercharged everything: [DeepMind's DQN][08] mastered Atari games in 2013, [AlphaGo][09] defeated the world Go champion in 2016, and by 2022 reinforcement learning from human feedback (RLHF) was powering [ChatGPT][10] and other large language models. In 2025, Barto and Sutton received the [ACM Turing Award][05] — computing's highest honor — for their foundational contributions to the field.

### Detailed History Timeline

- **1898** — [Edward Thorndike][01] (Columbia University) publishes his puzzle box experiments with cats, demonstrating that animals learn through trial and error. He formulates the [Law of Effect][02]: actions followed by satisfying outcomes are more likely to be repeated. This becomes the psychological bedrock of reinforcement learning.

- **1927** — [Ivan Pavlov][11] publishes *Conditioned Reflexes*, describing how dogs learn to associate a bell with food. While technically about classical conditioning (not reinforcement learning), Pavlov's work on stimulus-response associations deeply influences later learning theories.

- **1938** — [B.F. Skinner][03] publishes *The Behavior of Organisms*, introducing operant conditioning — the idea that behavior can be systematically shaped using reinforcement (rewards) and punishment. Skinner's "Skinner boxes" allow precise experimental control of animal learning. The very term "reinforcement" in reinforcement learning comes from this tradition.

- **1948** — [Claude Shannon][12] (Bell Labs) builds Theseus, a mechanical mouse that navigates a maze through trial and error using relay circuits. Many consider this the first physical demonstration of machine learning — a device that improves its performance through experience.

- **1950** — [Alan Turing][13] proposes in his landmark paper "Computing Machinery and Intelligence" that machines might learn through a process of reward and punishment, anticipating reinforcement learning decades before the algorithms existed.

- **1953** — [Richard Bellman][04] (RAND Corporation) develops dynamic programming and formulates the Bellman equation, which provides a mathematical framework for making sequences of optimal decisions. This equation becomes the theoretical backbone of reinforcement learning algorithms.

- **1954** — [Marvin Minsky][14] (Princeton/Harvard) writes his doctoral thesis on neural networks with reinforcement, one of the first works to connect psychological reinforcement principles to artificial learning systems. He recognizes that secondary reinforcers — intermediate signals that predict future reward — could be key to machine learning.

- **1960** — [Ronald Howard][15] publishes *Dynamic Programming and Markov Processes*, formally connecting Bellman's dynamic programming to Markov decision processes (MDPs) — the mathematical framework that describes environments where an agent makes decisions, transitions between states, and receives rewards. MDPs become the standard formalism for reinforcement learning problems.

- **1972** — [Klopf][16] at Wright-Patterson Air Force Base proposes that adaptive components within neural networks could act as "hedonistic neurons" that seek to maximize local reward signals. This work helps revive interest in trial-and-error learning within AI during a period when the idea had fallen out of favor.

- **1977** — [Ian Witten][17] (University of Essex) publishes the earliest known temporal-difference learning rule, proposing what is now called tabular TD(0) as part of an adaptive controller. This anticipates Sutton's later formalization but receives little attention at the time.

- **1981-1984** — [Andrew Barto and Richard Sutton][05] (University of Massachusetts Amherst) begin formalizing reinforcement learning as a computational framework. Sutton, Barto's PhD student, develops the actor-critic architecture — a design where one component (the actor) chooses actions and another (the critic) evaluates how good those actions were.

- **1988** — [Richard Sutton][06] publishes "Learning to Predict by the Methods of Temporal Differences," formally establishing temporal difference (TD) learning. TD methods allow an agent to learn from incomplete episodes — updating its estimates based on other estimates, without waiting for a final outcome. This is the key algorithmic innovation that separates RL from earlier approaches.

- **1989** — [Chris Watkins][07] (King's College London) develops Q-learning in his PhD thesis *Learning from Delayed Rewards*. Q-learning allows an agent to learn the value of actions directly, without needing a model of the environment. It is elegant, simple, and converges to optimal behavior under certain conditions — making it the most influential single algorithm in reinforcement learning.

- **1992** — [Watkins and Peter Dayan][18] publish a formal convergence proof for Q-learning, establishing its mathematical soundness and boosting confidence in the algorithm's reliability.

- **1992** — [Gerald Tesauro][19] (IBM) creates TD-Gammon, a backgammon-playing program that learns entirely through self-play using temporal difference learning. TD-Gammon reaches expert-level play and demonstrates that RL can master complex strategy games — a landmark result that inspires future game-playing AI.

- **1998** — [Sutton and Barto][20] publish *Reinforcement Learning: An Introduction* (MIT Press). The textbook unifies the field's scattered threads into a coherent framework and becomes the standard reference, eventually accumulating over 75,000 citations.

- **2000** — [Remi Munos and Andrew Moore][21] advance continuous-state reinforcement learning methods, extending RL beyond simple grid worlds to problems with smooth, high-dimensional state spaces — essential for real-world robotics and control.

- **2013** — [DeepMind][08] (Volodymyr Mnih and colleagues) publishes "Playing Atari with Deep Reinforcement Learning," introducing the Deep Q-Network (DQN). By combining Q-learning with deep neural networks, DQN learns to play dozens of Atari 2600 games directly from raw screen pixels, achieving human-level performance in many of them. This paper launches the deep reinforcement learning era.

- **2015** — DeepMind's DQN paper appears in [*Nature*][22], bringing deep RL to mainstream scientific attention. The same year, [AlphaGo][09] becomes the first program to defeat a professional Go player (Fan Hui, European champion).

- **2016** — [AlphaGo defeats Lee Sedol][09] 4-1 in Seoul, watched by an estimated 200 million viewers worldwide. Go had been considered far too complex for brute-force search — AlphaGo's victory, powered by deep RL and Monte Carlo tree search, is widely regarded as a watershed moment in AI.

- **2017** — [AlphaGo Zero][23] (DeepMind) learns Go entirely from self-play with no human game data, surpassing all previous versions within 40 days. The same year, [OpenAI][24] founds OpenAI Gym, a standardized toolkit for developing and comparing RL algorithms, accelerating research across the field.

- **2017** — [Schulman et al.][25] (OpenAI) introduce Proximal Policy Optimization (PPO), a policy-gradient algorithm that is simpler and more stable than earlier methods. PPO becomes the workhorse algorithm for many practical RL applications, including training language models.

- **2022** — [OpenAI releases ChatGPT][10], which uses reinforcement learning from human feedback (RLHF) — a technique where human preferences guide the RL reward signal — to align a large language model with user intent. RLHF, built on earlier work by [Christiano et al. (2017)][26] and [Ouyang et al. (2022, InstructGPT)][27], becomes the standard method for making AI assistants helpful and safe.

- **2025** — [Andrew Barto and Richard Sutton][05] receive the ACM A.M. Turing Award — often called the "Nobel Prize of computing" — for developing the conceptual and algorithmic foundations of reinforcement learning.

## 2. Application

### Brief Application Overview

Reinforcement learning spent its first few decades as a research curiosity — interesting in theory but limited to toy problems like simple grid worlds and tic-tac-toe. The transformation began in the 1990s when [Gerald Tesauro's TD-Gammon][19] showed that RL could master a genuinely complex game through self-play alone. But the real explosion came in the 2010s, when deep neural networks gave RL the ability to handle raw sensory input — pixels, audio, text — instead of hand-crafted features.

Today, RL is deployed across an extraordinary range of domains. In [gaming][08], it has conquered Atari, Go, chess, StarCraft, and Gran Turismo. In [robotics][28], it teaches arms to grasp objects, drones to fly, and legged robots to walk over rough terrain. [Google uses RL][29] to reduce data center cooling costs by up to 40%. [Autonomous vehicles][30] from Wayve and others use deep RL for navigation decisions. In [healthcare][31], RL optimizes drug dosing, ICU ventilator settings, and personalized treatment plans.

Perhaps the most surprising application arrived in 2022: RLHF became the key technique for making [large language models like ChatGPT][10] behave helpfully and safely. By treating human preference as a reward signal, RL now shapes the AI tools that millions of people use daily. The [global RL market][32] is projected to grow from $0.49 billion in 2023 to $3.83 billion by 2030, reflecting how rapidly the technology is moving from labs to products.

### Detailed Application Timeline

- **1959** — [Arthur Samuel][33] (IBM) demonstrates a checkers-playing program that improves through self-play, using techniques that anticipate modern RL. Samuel's program is one of the earliest examples of a machine learning from experience rather than being explicitly programmed.

- **1992** — [Gerald Tesauro][19] (IBM Research) creates TD-Gammon, which learns backgammon through 1.5 million games of self-play using temporal difference learning. It reaches expert human-level play and influences professional backgammon strategy — one of the first cases of an RL system teaching humans something new about a game.

- **1992** — [Mahadevan and Connell][34] demonstrate the OBELIX robot learning to push boxes to target locations using RL, one of the earliest applications of reinforcement learning to physical robotics.

- **1994** — A [Zebra Zero robot arm][35] learns peg-in-hole insertion tasks using RL, demonstrating that trial-and-error learning can handle precise manipulation tasks that are difficult to program explicitly.

- **1996** — [Schaal][36] uses RL to teach a Sarcos humanoid robot arm to balance a pole — a classic control problem — demonstrating that RL can work on real hardware with continuous state spaces.

- **2001** — [Andrew Ng and colleagues][37] (Stanford) use RL to train an autonomous helicopter to perform aerobatic maneuvers, including inverted flight. The helicopter learns behaviors that exceed what human pilots can reliably demonstrate, showcasing RL's potential in aerospace.

- **2013** — [DeepMind][08] demonstrates DQN playing Atari 2600 games from raw pixels, achieving superhuman performance in games like Breakout and Pong. This is the first time a single RL algorithm learns multiple complex tasks from high-dimensional sensory input, launching the deep RL applications era.

- **2014** — [Google][29] begins applying RL to data center cooling optimization. Machine learning algorithms learn to adjust fans, cooling systems, and windows based on sensor data, eventually reducing cooling energy consumption by up to 40% — saving millions of dollars annually and significantly reducing carbon emissions.

- **2016** — [DeepMind's AlphaGo][09] defeats world Go champion Lee Sedol 4-1 in a match watched by 200 million people. Go has approximately 10^170 possible board positions — far more than atoms in the universe — making brute-force search impossible. AlphaGo's victory proves that RL combined with deep learning can handle problems previously thought intractable.

- **2017** — [OpenAI Five][38] begins development — an RL system that will eventually defeat the world champion team in Dota 2 (2019), a complex multiplayer video game requiring long-term strategy, teamwork, and real-time decision-making over 45-minute matches.

- **2017** — [AlphaGo Zero][23] (DeepMind) achieves superhuman Go play through pure self-play — no human game data at all. After 40 days of training, it defeats the version that beat Lee Sedol. Later in 2017, [AlphaZero][39] generalizes this approach to chess and shogi as well, mastering all three games from scratch.

- **2018** — [Wayve][30] (London) begins testing autonomous vehicles on public roads using deep RL. Unlike most self-driving companies that rely on hand-coded rules, Wayve trains its driving policy end-to-end from camera input, initially on a 250-meter stretch of road.

- **2018** — [OpenAI's Dactyl][40] uses RL to train a robotic hand (Shadow Dexterous Hand) to manipulate a Rubik's cube, learning entirely in simulation and then transferring the policy to the real robot — a landmark demonstration of sim-to-real transfer.

- **2019** — [Loon (Alphabet/Google)][41] deploys RL to control stratospheric balloons that provide internet access to remote areas. RL agents learn to navigate wind patterns at different altitudes to keep balloons positioned over target coverage areas — a real-world control problem with complex, unpredictable dynamics.

- **2020** — [DeepMind's Agent57][42] becomes the first RL agent to achieve above-human performance on all 57 Atari games in the standard benchmark, closing a gap that had persisted since the original DQN paper.

- **2020** — [DeepMind applies RL to nuclear fusion][43] — specifically, controlling the plasma in a tokamak reactor at the Swiss Plasma Center. The RL controller learns to shape and maintain the superheated plasma, achieving performance comparable to hand-tuned controllers developed over years.

- **2021** — [Google][44] uses RL for chip design, training agents to place transistors on computer chips. The RL system generates chip layouts in hours that match or exceed the quality of layouts created by human engineers over weeks — potentially accelerating the semiconductor design cycle.

- **2022** — [Sony AI's Gran Turismo Sophy][45] defeats world-champion human drivers in the racing game Gran Turismo Sport. The agent is trained entirely in simulation using deep RL and deployed without modification — demonstrating that RL can master tasks requiring split-second physical intuition.

- **2022** — [OpenAI releases ChatGPT][10], fine-tuned using RLHF. Human raters compare pairs of model responses, their preferences train a reward model, and PPO optimizes the language model against that reward signal. ChatGPT reaches 100 million users in two months, making RLHF the most widely impactful RL application to date.

- **2023-present** — RLHF becomes standard practice across the AI industry. [Anthropic's Claude][46], [Google's Gemini][47], and [Meta's Llama][48] all use RL-based alignment techniques. Variants like DPO (Direct Preference Optimization) and RLAIF (RL from AI Feedback) emerge, extending the paradigm. RL is now central to making AI assistants helpful, harmless, and honest.

- **2023-present** — [Healthcare applications][31] of RL expand: optimizing chemotherapy dosing, personalizing insulin delivery for diabetes patients, managing ICU ventilator settings, and guiding clinical decision-making. While many remain in clinical trials, RL is increasingly viewed as a tool for precision medicine.

## 3. Key Figures

| Person | Years | Contribution |
|:-------|:------|:-------------|
| Edward Thorndike | 1874-1949 | Established trial-and-error learning and the Law of Effect through puzzle box experiments with cats |
| B.F. Skinner | 1904-1990 | Formalized operant conditioning — behavior shaped by reinforcement and punishment — giving RL its name |
| Richard Bellman | 1920-1984 | Developed dynamic programming and the Bellman equation, the mathematical foundation for optimal sequential decisions |
| Marvin Minsky | 1927-2016 | Early work connecting psychological reinforcement to artificial learning systems |
| Andrew Barto | 1948-present | Co-developed temporal difference learning and the actor-critic architecture; co-authored the foundational RL textbook; 2024 Turing Award |
| Richard Sutton | 1956-present | Formalized TD learning, policy gradient methods, and the RL problem framework; co-authored the foundational textbook; 2024 Turing Award |
| Chris Watkins | 1960-present | Invented Q-learning (1989), the most influential single algorithm in reinforcement learning |
| Gerald Tesauro | — | Created TD-Gammon (1992), proving RL could master complex strategy games through self-play |
| Volodymyr Mnih | — | Lead author of DeepMind's DQN paper (2013), launching the deep reinforcement learning era |

## 4. Connection to This Workshop

Reinforcement learning is directly relevant to the autonomous robot workshop, even though the first iterations use simpler control methods. The line-following robot's progression from analog comparators (Iteration #1) to PID control (Iteration #4) mirrors the historical progression of control strategies that RL eventually learned to discover on its own. A line-following robot is, at its core, an agent (the robot) sensing an environment (the track), taking actions (motor adjustments), and receiving feedback (staying on or drifting off the line) — exactly the reinforcement learning framework. In future iterations or advanced projects, students could replace the hand-tuned PID controller with an RL agent that learns its own control policy through trial and error on the track.

## 5. Evolution Diagram

```
Animal Psychology          Mathematical Optimization         Computer Science
     │                            │                               │
Thorndike's                 Bellman's Dynamic              Shannon's Theseus
Law of Effect               Programming                    Maze Mouse
  (1898)                      (1953)                         (1950)
     │                            │                               │
Skinner's Operant           Markov Decision                 Minsky's Neural
Conditioning                Processes                       Reinforcement
  (1938)                      (1960)                         (1954)
     │                            │                               │
     └────────────┬───────────────┘                               │
                  │                                               │
           Barto & Sutton                                         │
           Actor-Critic                                           │
            (1981-84)                                             │
                  │                                               │
           Sutton's TD Learning (1988) ◄──────────────────────────┘
                  │
           Watkins' Q-Learning (1989)
                  │
           TD-Gammon (1992)
                  │
           Sutton & Barto Textbook (1998)
                  │
           Deep Q-Network / DQN (2013)
                  │
     ┌────────────┼────────────┐
     │            │            │
  AlphaGo     Robotics      RLHF &
  (2016)      (2018+)      ChatGPT
                            (2022)
```

## 6. Sources & References

[01]:https://www.simplypsychology.org/edward-thorndike.html
[02]:https://en.wikipedia.org/wiki/Law_of_effect
[03]:https://en.wikipedia.org/wiki/Operant_conditioning
[04]:https://en.wikipedia.org/wiki/Richard_E._Bellman
[05]:https://www.acm.org/media-center/2025/march/turing-award-2024
[06]:https://www.researchgate.net/publication/220344150_Technical_Note_Q-Learning
[07]:https://www.cs.rhul.ac.uk/~chrisw/RL_some_history.html
[08]:https://arxiv.org/abs/1312.5602
[09]:https://deepmind.google/discover/blog/deep-reinforcement-learning/
[10]:https://intuitionlabs.ai/articles/key-innovations-behind-chatgpt
[11]:https://en.wikipedia.org/wiki/Ivan_Pavlov
[12]:https://en.wikipedia.org/wiki/Theseus_(maze-solving_machine)
[13]:https://en.wikipedia.org/wiki/Computing_Machinery_and_Intelligence
[14]:https://en.wikipedia.org/wiki/Marvin_Minsky
[15]:https://en.wikipedia.org/wiki/Ronald_A._Howard
[16]:https://en.wikipedia.org/wiki/Reinforcement_learning
[17]:https://en.wikipedia.org/wiki/Ian_H._Witten
[18]:https://link.springer.com/article/10.1007/BF00992698
[19]:https://en.wikipedia.org/wiki/TD-Gammon
[20]:https://mitpress.mit.edu/9780262193986/reinforcement-learning/
[21]:https://en.wikipedia.org/wiki/Reinforcement_learning
[22]:https://www.nature.com/articles/nature14236
[23]:https://deepmind.google/discover/blog/alphago-zero-starting-from-scratch/
[24]:https://github.com/openai/gym
[25]:https://arxiv.org/abs/1707.06347
[26]:https://arxiv.org/abs/1706.03741
[27]:https://arxiv.org/abs/2203.02155
[28]:https://www.ri.cmu.edu/pub_files/2013/7/Kober_IJRR_2013.pdf
[29]:https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/
[30]:https://wayve.ai/
[31]:https://www.mdpi.com/2218-6581/2/3/122
[32]:https://www.q3tech.com/blogs/applications-of-reinforcement-learning/
[33]:https://en.wikipedia.org/wiki/Arthur_Samuel_(computer_scientist)
[34]:https://www.ri.cmu.edu/pub_files/2013/7/Kober_IJRR_2013.pdf
[35]:https://www.ri.cmu.edu/pub_files/2013/7/Kober_IJRR_2013.pdf
[36]:https://www.ri.cmu.edu/pub_files/2013/7/Kober_IJRR_2013.pdf
[37]:https://en.wikipedia.org/wiki/Andrew_Ng
[38]:https://openai.com/index/openai-five/
[39]:https://deepmind.google/discover/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/
[40]:https://openai.com/index/solving-rubiks-cube/
[41]:https://blog.x.company/drifting-efficiently-through-the-stratosphere-using-deep-reinforcement-learning-c38723ee2e90
[42]:https://deepmind.google/discover/blog/agent57-outperforming-the-human-atari-benchmark/
[43]:https://deepmind.google/discover/blog/accelerating-fusion-science-through-learned-plasma-control/
[44]:https://www.nature.com/articles/s41586-021-03544-w
[45]:https://www.gran-turismo.com/us/gran-turismo-sophy/
[46]:https://www.anthropic.com/
[47]:https://deepmind.google/technologies/gemini/
[48]:https://ai.meta.com/llama/
