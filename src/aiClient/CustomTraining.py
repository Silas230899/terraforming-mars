import torch
import torch.nn as nn
import random
from torch.distributions import Categorical
import numpy as np
import torch.optim as optim

from CustomEnvironment import CustomEnv
from CustomModel import ActorCritic

from stable_baselines3 import PPO

# Trajectory-Speicher
def collect_trajectories(env, model, num_episodes):
    trajectories = []
    for _ in range(num_episodes):
        state, _ = env.reset()
        episode = {"states": [], "actions": [], "rewards": [], "log_probs": [], "values": []}

        state_tensor = torch.tensor(
            np.concatenate([state[key] for key in state.keys()]),
            dtype=torch.float32
        )
        done = False

        while not done:
            # Modellvorhersage
            probs, value = model(state_tensor)
            dist = Categorical(probs)
            action = dist.sample()

            # Daten sammeln
            log_prob = dist.log_prob(action)
            episode["states"].append(state_tensor)
            episode["actions"].append(action)
            episode["log_probs"].append(log_prob)
            episode["values"].append(value)

            # Nächsten Zustand abrufen
            next_state, reward, done, _, _ = env.step(action.item())
            episode["rewards"].append(reward)

            # Zustand aktualisieren
            state_tensor = torch.tensor(
                np.concatenate([next_state[key] for key in next_state.keys()]),
                dtype=torch.float32
            )

        trajectories.append(episode)
    return trajectories

# Training mit Batches (Korrektur)
def train_with_batches(env, model, optimizer, num_episodes, batch_size, epochs, gamma=0.99):
    # Trajektorien sammeln
    trajectories = collect_trajectories(env, model, num_episodes)

    # Berechnung von Returns und Vorteilen pro Episode
    all_returns = []
    all_advantages = []
    all_states = []
    all_actions = []
    all_log_probs = []

    for episode in trajectories:
        rewards = episode["rewards"]
        values = torch.stack(episode["values"])
        G = 0
        returns = []
        advantages = []

        # Rückwärts durch die Episode iterieren
        for reward, value in zip(reversed(rewards), reversed(values)):
            G = reward + gamma * G
            returns.insert(0, G)
            advantages.insert(0, G - value.item())

        all_returns.extend(returns)
        all_advantages.extend(advantages)
        all_states.extend(episode["states"])
        all_actions.extend(episode["actions"])
        all_log_probs.extend(episode["log_probs"])

    # Konvertierung in Tensoren
    all_states = torch.stack(all_states)
    all_actions = torch.tensor(all_actions, dtype=torch.long)
    all_log_probs = torch.stack(all_log_probs)
    all_returns = torch.tensor(all_returns, dtype=torch.float32)
    all_advantages = torch.tensor(all_advantages, dtype=torch.float32)

    # Training in Batches
    dataset = list(zip(all_states, all_actions, all_log_probs, all_advantages, all_returns))
    for epoch in range(epochs):
        random.shuffle(dataset)
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            batch_states, batch_actions, batch_log_probs, batch_advantages, batch_returns = zip(*batch)

            # Tensoren erstellen
            batch_states = torch.stack(batch_states)
            batch_actions = torch.stack(batch_actions)
            batch_log_probs = torch.stack(batch_log_probs)
            batch_advantages = torch.tensor(batch_advantages)
            batch_returns = torch.tensor(batch_returns)

            # Modell-Update
            optimizer.zero_grad()
            new_probs, new_values = model(batch_states)
            dist = Categorical(new_probs)
            new_log_probs = dist.log_prob(batch_actions)

            # PPO-Objektiv
            ratio = torch.exp(new_log_probs - batch_log_probs)
            policy_loss = -torch.min(
                ratio * batch_advantages,
                torch.clamp(ratio, 1 - 0.2, 1 + 0.2) * batch_advantages
            ).mean()
            value_loss = nn.functional.mse_loss(new_values.squeeze(), batch_returns)
            loss = policy_loss + 0.5 * value_loss

            # Backpropagation
            loss.backward()
            optimizer.step()

# Setup für Environment und Modell
env = CustomEnv()
model2 = PPO("MlpPolicy", env)
model2.learn(total_timesteps=10_000)
model = ActorCritic(env.observation_space, env.action_space)
optimizer = optim.Adam(model.parameters(), lr=3e-4)


# Training ausführen
train_with_batches(
    env=env,
    model=model,
    optimizer=optimizer,
    num_episodes=500,  # Anzahl der Episoden für Sampling
    batch_size=32,  # Batch-Größe
    epochs=10,  # Anzahl der Durchläufe über die Daten
    gamma=0.99  # Diskontierungsfaktor
)
