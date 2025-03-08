"""
Main entry point for the Snake Game web deployment.
This file imports and runs the actual game code from snake_game.py.
"""
import asyncio
from snake_game import main

# For Pygbag web deployment
asyncio.run(main())
