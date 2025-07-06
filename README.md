# MuQ
> MuQ is a web-application to make events with background music more interative.

## Table of Contents
- [MuQ](#muq)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [No login required](#no-login-required)
    - [Using Spotify](#using-spotify)
  - [The idea](#the-idea)
    - [Why not use this system for bigger events?](#why-not-use-this-system-for-bigger-events)
  - [Why should you use MuQ?](#why-should-you-use-muq)
    - [Easy to use](#easy-to-use)
    - [Fast and relyable](#fast-and-relyable)
    - [No login required](#no-login-required-1)
    - [Open Source Software](#open-source-software)
  - [Installation](#installation)
    - [Basic needs](#basic-needs)
    - [Clone the repository](#clone-the-repository)
      - [1. Using **git**](#1-using-git)
      - [2. From GitHub directly](#2-from-github-directly)
  - [Running MuQ](#running-muq)
    - [Add a new app on Spotify](#add-a-new-app-on-spotify)
    - [.env file](#env-file)
      - [Make the .env file](#make-the-env-file)
      - [Set up your .env file](#set-up-your-env-file)
    - [Rye setup](#rye-setup)
    - [Building the css](#building-the-css)
    - [Running the development server](#running-the-development-server)


## Overview
MuQ is a web-app to make events, festivals, parties etc. more interactive. With this app, users can easily add or vote for songs that should be played next. Additionally, users can keep track of their wished songs and can monitor, when it will be played next.

### No login required
With MuQ, you can use all features without needing to set a password or login with personal data. When a new device connects with the MuQ server, the server gives the device a id, so that songs that are requested can be remembered.

### Using Spotify
Spotify is the biggest music streaming service and has millions songs and MuQ takes full adventage of the possibilities given by the Spotify API. 

You only need to have a spotify premium account and you can connect your account with MuQ. You only need 2 things to use your account:
- A client id
- A client secret

Where you can request them ([Spotify Developer](#spotify-developers)) and how to tell MuQ ([.env file](#env-file)) are being discussed later.

## The idea
The idea started on a night with friends when we had a speaker to hear some music while talking. We had a Spotify Jam open, so that everyone at the meetup can put in some music they want to hear. But there was one problem: When you missclick on a song it directly plays. This happened pretty often. Additionally, there where too many settings, that could be changed by accident. For the most part they wheren't even necessary for the most use cases.

I thought about a way to have the necessary functionality of putting a song into a queue but limit the possible damage someone can do, by missclicking on a song or button. 

### Why not use this system for bigger events?
At many different café's in germany, I found a system where you can request songs. I tried it ones and I directly notised, that you needed an account to use this software. This bothered me.

When I had the idea for MuQ, I remembered that situation. I found the idea of requesting a song to be played at an event interesting. And I am not the only one: Why do people request songs at the club? It is the same principle: **Inclusion** 

**They want to be a part of the event.**

We included the idea of using MuQ into the concept. Our goal: Make a easy to use system, without having anyone to sign up or log in to use it. It should be as easy to just scan a QR-Code and **boom**. You can start requesting your favourite songs. Furthermore, the user should only have the functionality that they need so that they can't break or interfear with the current music playback. 

## Why should you use MuQ?
When you came this far and you are unsure, if you should use MuQ, this topic is just for you. 

You should use MuQ, if you are
- ... a party host, that wants to include people into your music selection.
- ... a member of a friend group that wants to make group meetups just a bit better.
- ... a member of a friend group that is conserned that their music selection is not for everyone.
- ... a party host that is unsure, if their music selection is good.
- ... a party host that only has very "special" playlists to pick from.
- ... someone that thinks Jams are to unsafe for bigger groups of people.
- ... **a good person**

Okay, if you are still unsure (so you are not a good person?), MuQ has some good arguments, why you should use it.

### Easy to use
MuQ is an intuitive and easy to use system that is designed to be used by everyone. With a clear interface it is easy to find functionality and information with just one tap. No burger menus or overloaded pages. MuQ uses a tap system to seperate different parts of functionality. Those taps can be changed by buttons in a 1:1 format (one button -> one tap) that are found on the bottom of the webpage. Not even one click away.

### Fast and relyable
When developing MuQ, our number one prioity was builing a fast user interfase (UI). Suprisingly this isn't very common for web-apps. We wanted an instantanious experience, where tap changes and information updates feel instant. We had one main rule: **It should feel like an application that is installed on your device. Not like a web-application.**

MuQ is also relyable. It is build with a *server send event stream* (SSE) that streams live information to the client. This SSE stream is build to be relyable. Even when:
- The device disconnects from the internet for a few minutes
- The SSE stream stops
- A server error (500) occures
- Packets are lost
- The server is offline for a short period of time

... **the MuQ client still works, without having to reload it.**

### No login required
To use MuQ, you don't have to login or sign up. You just open up the web-application and there you go. **All our functionality. In the palm of your hand.**

MuQ automatically sets a cookie with a id, when a device with no such cookie is found. With that, MuQ can understand which device requested with song and can also remember it when you reload the page or leave it. When you come back. Your data is still there.

### Open Source Software
Unlike other software solutions, we **publish all our source code** so that everyone can see what our software does and can contribute to the project.

**Problems and errors in our software can also be found faster than in a closed development environment**. So that our software can be as stable and secure as possible. This is crucial for future development. 

## Installation
### Basic needs
Before you can think about cloning the project to your local machine you'll need:
- Rye 

You can install Rye here: [Download](https://rye.astral.sh/guide/installation/)

Check your Rye installation with this command:
```bash
rye --version
```

The console should return something like this:
```bash
rye 0.34.0
commit: 0.34.0 (d31340178 2024-05-20)
platform: windows (x86_64)
self-python: cpython@3.12.3
symlink support: false
uv enabled: true
```

**Okay, nice.**

>#### Why Rye?
>We use Rye as a tool to manage python venv's (Virtual environments) and dependencies. Installing dependencies and managing your python venv's can be difficult and frustrating. Rye helps by installing python and building venv's for you. 
>
>With Rye it is also easy to share your projects with others. **They can set up your project with only one command.**
>
>Enough fantasising about Rye. Back to our installation process.

### Clone the repository
>Now you need our source code. **No code. No fun.** You can clone our code from GitHub in two different ways:
#### 1. Using [**git**](https://git-scm.com/)
Make sure you have [**git**](https://git-scm.com/) installed on your device. If not install it or use the second method:
```bash
git --version
```

Use this command to clone our repository onto your local machine:
```bash
git clone https://github.com/LuisSchuimer/MuQ
```
This will download our repository into your current directory.

#### 2. From GitHub directly
If you don't have **git** installed on your machine you can download it directly from your browser:
```
https://github.com/LuisSchuimer/MuQ/archive/refs/heads/main.zip
```
This should download the source code as a .zip archive into your download folder. Now unpack this archive and you are ready to go.

## Running MuQ

### Add a new app on Spotify
>To use MuQ, you need to connect your account with our software. But we can't just take your login credentials and connect your account that way. You need to make a new app on Spotify. To do that you'll need a **Spotify Premium Account**. 

Here is a step by step guide on how to get there:
1. Open the [Spotify Developer](https://developer.spotify.com/) website and login with your account.
2. Click on your profile name and go to "**Dashboard**" or click [here](https://developer.spotify.com/dashboard)
3. Click on "**Create App**" or click [here](https://developer.spotify.com/dashboard/create)
4. Fill out "**App name**" and "**Description**" after your liking
5. For the Redirect URIs you'll need to fill in:
   ```
   http://127.0.0.1:8000/callback
   ```
   and click "**Add**"
6. Check the "**Web API**", so that MuQ can access this API endpoint with this app
7. Agreethe Spotify's Developer Terms of Service and Design Guidelines
8. Click "**Save**"

**You created an app on Spotify that MuQ can use. Good job.**

After you created this app, you'll see a new page, where all information about your new app can be seen. Note down two values, that we'll need at the next step:
- Client ID (Can be found directly)
- Client Secret (Hidden under a button)

Don't worry, those values can be looked up any time you want. Just press on your app on the Dashboard and you can look them up.

### .env file
>When you successfuly created your app, you'll need to tell MuQ how to connect to your account. You need to do that with a .env file.
>
>**You mide ask: "Why use a .env file?"**
>
>Often, Developers publish their Client IDs or API informations that should stay private, because they leave them inside of their code. We use .env as a safety feature and as an easy way to manage consants that don't change during the programs runtime. 
>
>Because .env files where developed to prevent Client ID or API key leakage, git can ignore them, so that they aren't automatically pushed to the repository.

#### Make the .env file
To use our software, you'll need a .env file. **Make this file in the root of the project**. To ensure you are in the right place, look if you can see the **README.md** file without having to change your directory. If you see that folder, you are in the right place. 

#### Set up your .env file
Okay, know you need to open this file in an editor (VSC or else) and set your .env file up. To do that copy this template into your file:
```
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
```
Fill in your Client ID and Client Secret you noted down earlier into the quotation marks. Save this file and you are **almost done**.

### Rye setup
>To run MuQ you only need to run three more commands. Those commands install python, sets up a virtual environment and most importantly: **Installs dependencies**. 
>
>Without dependencies MuQ wouldn't work as easily as it is. We use **flask** and other modules (dependencies) to make our application work. This makes the development process much easier, because we don't have to code everything on our own. We can rely on other peoples implementation for **webservers** etc.
>
>Let's install those dependencies, **Shall we?**

To sync all dependencies with our venv, we need to run
```bash
rye sync
```
in the root of our project (where the .env file is located).

This command should now install python, set everything up and install our dependencies. When the process was successful, the last line should say:
```
Done!
```

### Building the css
>We don't use standart css. We use a framework called "Tailwind CSS" it helps us create better and more modern styling with less code. It is a nice helper, to make beautiful and modern interfaces. But before we can adore the beauty of our web-application, we need to build the css. If we don't do that, we won't have any nice styling. **We don't want that to happen, right?**

You can build the CSS with Rye. Just run:
```bash
rye run css-build
```
This should install and build the CSS. The Output should look like this:
```
[INFO]: Getting latest tailwind-cli-extra version ...
≈ tailwindcss v4.1.11

/*! 🌼 daisyUI 5.0.43 */
Done in 126ms
```
**Nice work! Only one step away from success!**

### Running the development server
To run the MuQ development server just run:
```bash
rye run dev
```
This command should start the server and you should see something like this in the console:
```
YOUR_CLIENT_ID
YOUR_CLIENT_SECRET
You need to authenticate your Spotify: YOUR_AUTH_LINK <- Your auth link
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000 <- Use this on your local device
 * Running on http://192.168.179.4:8000 <- Use this on other devices in your network
Press CTRL+C to quit
```

To now use MuQ for the first time, click on the **auth link** to authenticate MuQ at the Spotify Account Management. If you did that. You should see a new line like this, displayed in the console:
```
127.0.0.1 - - [07/Jul/2025 01:38:59] "GET /callback?code=YOUR_AUTH_TOKEN HTTP/1.1" 200 -
```
Now, you can go on **http://127.0.0.1:8000** on your device or (if your router allows this) access the web-app from **another device in the same network**. 

You can now play some music with the Spotify player **(make sure you use the same account you used to create your app)**

**Great job. You installed and ran MuQ for the first time!**