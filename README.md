# Reinforcement Learning Agent in Python

## Overview
This AI uses principles of [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning) to generate a strategy for playing tic-tac-toe. The AI agent plays against itself for thousands of games and uses the fact of winning, losing or drawing each game to update the values associated with each state in the state space. The program then gives the end user the opportunity to play against the AI agent.

## Algorithm
Initially the AI agent determines values of each possible state in the game. If the state is a winning state for the agent we assign 1, if there is no clear winner then we assign .5 and if it is a losing state we assign 0.

As the AI agent plays game after game it modifies the values associated with each state. This is done by storing a list of the states that we have visited during a game. If we win that game then all of the states that lead to victory will have their associated values increased. The opposite is the case if we lose.

The approach that dictates how this AI learns is the epsilon greedy approach. This is a method commonly used to solve the [multi-armed bandit](https://en.wikipedia.org/wiki/Multi-armed_bandit) problem. The epsilon greedy algorithm dictates that we should choose a probability (eg 10%) in which we will take a random action. The rest of the time we will choose the best action. This allows the AI to explore different routes to victory over time.

