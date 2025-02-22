# Discord Selfbot

A simple Discord bot that provides useful utilities like AFK mode and Spotify song sharing. This bot is designed to run as a proper bot account, not a user account automation tool.

## Features

- AFK mode with customizable away messages
- Current Spotify song sharing
- Eval command for bot owners
- Owner-only command restrictions

## Setup

1. Create a `.env` file with your bot token:
   ```
   token=YOUR_BOT_TOKEN_HERE
   ```

2. Configure `config/config.json`:
   ```json
   {
       "prefix": ".", 
       "main_account_id": "YOUR_USER_ID_HERE",
       "spotify_token": "YOUR_SPOTIFY_TOKEN_HERE",
       "afk": {
           "enabled": false,
           "message": "I am not available right now."
       }
   }
   ```

3. To get your Spotify token:
   - Visit https://spotify-overlay.raphaelmarco.com/
   - Log in with your Spotify account
   - After logging in, copy the access token from the URL
   - Paste it into the `spotify_token` field in config.json

## Usage

- `.afk` - Toggle AFK mode
- `.send-song` - Share your current Spotify song
- `.eval` - Execute code (bot owner only)

## Note

This bot is intended to be run as a proper Discord bot account. It does not automate user accounts, which would violate Discord's Terms of Service.
