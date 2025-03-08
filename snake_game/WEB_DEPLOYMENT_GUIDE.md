# Web Deployment Guide for Ultimate Snake Game

This guide will help you deploy your Snake Game to the web so others can play it in their browsers without installing anything.

## Prerequisites

- Python 3.8 or newer
- Pygame installed
- Internet connection

## Step 1: Install Pygbag

Pygbag is the tool that converts your Pygame game to WebAssembly so it can run in a browser.

Run the `install_pygbag.bat` file included with your game, or manually install it using pip:

```
pip install pygbag
```

## Step 2: Test Locally

Before deploying, test your game on the local web server:

1. Run the `run_pygbag.bat` file
2. Open your browser and go to http://localhost:8000
3. Verify your game works correctly in the browser

## Step 3: Create Web Build

Once you've tested and everything works properly:

1. Run the `build_web.bat` file
2. This will create a `build` folder containing your web-ready game
3. Inside the `build` folder, you'll find a `web.zip` file ready for deployment

## Step 4: Deploy to itch.io (Recommended)

itch.io is a popular platform for indie games and the easiest way to share your Snake Game:

1. Go to [itch.io](https://itch.io/) and create an account if you don't have one
2. Click "Upload a new project" from your dashboard
3. Fill in the details for your game (title, description, etc.)
4. Under "Kind of project", select "HTML"
5. Under "Upload files", upload the `web.zip` file from your `build` folder
6. Check "This file will be played in the browser"
7. Click "Save & view page" to publish your game
8. Your Snake Game is now available for anyone to play online!

## Step 5: Deploy to Other Platforms (Optional)

### GitHub Pages

If you have a GitHub account:

1. Create a new repository or use an existing one
2. Extract the contents of `web.zip` to a folder in your repository
3. Enable GitHub Pages in your repository settings
4. Your game will be available at `https://[your-username].github.io/[repository-name]`

### Your Own Web Server

If you have access to a web server:

1. Extract the contents of `web.zip` to a directory on your web server
2. Make sure the directory is accessible via HTTP
3. Your game will be available at your domain name

## Troubleshooting

- **Game runs slowly or has audio issues**: Try a different browser; Chrome and Edge typically have the best WebAssembly performance
- **Loading takes too long**: The first load might take some time as the WebAssembly compiles; subsequent loads should be faster
- **Game doesn't load at all**: Check browser console for errors; make sure your browser supports WebAssembly

## Customizing the Web Page

If you want to customize how your game looks on the web:

1. Edit the `index.html` file in your Snake Game folder
2. Customize the styles, add more information, etc.
3. Rebuild using `build_web.bat`

## Technical Details

Pygbag converts your Python/Pygame code to WebAssembly using Emscripten, allowing it to run in modern browsers. The asynchronous modifications we've made to your game code ensure it runs smoothly in this environment.

Your game now uses the browser's event loop instead of Pygame's, which is why we added `await asyncio.sleep(0)` at critical points in your code.
