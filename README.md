# Tactical Ops AI

## Bot Description
Tactical Ops AI is a multimodal strategy advisor designed to simulate an elite eSports coach by analyzing game states through screenshots and user queries to deliver precise, victory-oriented guidance. It leverages OpenRouter to route requests across multiple advanced Vision-Language Models (VLMs) (including Gemini, LLaMA, and Qwen), allowing dynamic model selection based on tactical depth, visual complexity, and response speed. The system intelligently adapts responses for various gaming genres—ranging from RPGs to strategy and puzzles—using contextual conversation memory and visual evidence analysis to provide accurate, high-level strategic advice in real time.

## Features

- **AI-Powered Strategy Advisor**
  Simulates professional coaching by delivering concise, tactical, and victory-oriented advice tailored to the specific game state.

- **Multi-Model AI Support**
  Routes requests through OpenRouter, enabling dynamic selection between multiple advanced AI and vision models based on reasoning capabilities and visual acuity.

- **Vision-Based State Analysis**
  Analyzes uploaded game screenshots using vision-capable models to interpret HUDs, maps, board states, inventory screens, and enemy positions.

- **Genre-Aware Tactics**
  Adapts strategic advice dynamically for RPGs, FPS, MOBA, Puzzle/Logic games, and Retro titles to match the specific mechanics and pacing of the genre.

- **Real-Time Streaming Responses**
  Streams AI-generated responses live to provide immediate feedback, minimizing downtime during gameplay.

- **Contextual Conversation Memory**
  Maintains recent chat history to enable follow-up questions about the current game state without needing to re-upload evidence.

- **Immersive Gamer Interface**
  Custom-styled "Hacker Terminal" UI built with Streamlit and custom CSS, featuring a dark mode aesthetic and tactical typography for an immersive user experience.

- **Model Failover & Reliability Controls**
  Allows manual model switching and visual feedback on connection status to ensure consistent availability during gaming sessions.

- **Secure Environment Configuration**
  Uses environment variables and secrets management to protect API keys and configuration data.

## Supported Theater of Operations (Game Genres)

Tactical Ops AI is designed to handle a wide range of gaming scenarios by dynamically adapting its analysis and persona based on the selected genre.

- **RPG / Open World**
  Analyzes quests, inventory management, boss mechanics, and exploration routes for optimal progression.

- **FPS / Competitive**
  Provides advice on positioning, map awareness, loadout optimization, and counter-tactics based on visual cues.

- **MOBA / Strategy**
  Evaluates board states, unit composition, resource management, and macro-strategy for competitive advantage.

- **Puzzle / Logic**
  Solves complex visual puzzles, chess positions, and logic gates by interpreting the visual rules of the challenge.

- **Retro / Arcade**
  Offers classic tips, pattern recognition, and high-score strategies for vintage gaming titles.

## License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project for personal or commercial purposes, provided that the original copyright notice and license are included.

This project is intended for educational and experimental use and is provided **“as is”**, without warranty of any kind.
