import numpy as np
import tensorflow as tf
from collections import deque


class Learn:
    def __init__(self, env, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, 
                 gamma=0.95, learning_rate=0.001, batch_size=32, memory_size=10000, 
                 target_update_frequency=100):
        
        self.env = env
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.target_update_frequency = target_update_frequency
        self.model = self._build_model()
        self.target_model = tf.keras.models.clone_model(self.model)
        self.target_model.set_weights(self.model.get_weights())
        self.target_update_counter = 0
    
    
    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, input_shape=self.env.observation_space_shape(), activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.env.action_space_size())
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model
    
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    
    def _update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())
    
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return self.env.get_random_action()
        else:
            return np.argmax(self.model.predict(state)[0])
    
    
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in batch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                target[0][action] = reward + self.gamma * np.max(self.target_model.predict(next_state)[0])
            self.model.fit(state, target, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    
    def RL(self, num_episodes):
        for episode in range(num_episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.env.observation_space_size()])
            total_reward = 0
            done = False
            while not done:
                action = self.act(state)
                next_state, reward, done = self.env.step(action)
                next_state = np.reshape(next_state, [1, self.env.observation_space_size()])
                self.remember(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                self.replay()
                if self.target_update_counter % self.target_update_frequency == 0:
                    self._update_target_model()
                self.target_update_counter += 1
            print(f"Episode: {episode + 1}, Total Reward: {total_reward}")
            
            
