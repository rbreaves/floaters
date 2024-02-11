# Floaters (Windows only)
Provides a mechanism to allow users to shift focus from a fullscreen remote application to the host OS. Examples would be running RDP fullscreen or a VNC client such as RealVNC.

## The Problem
Many applications that allow you to redirect all keyboard input often times don't have an easy or reliable way of jumping back out that is simple and easy, as to avoid breaking your workflow.

## The Solution
This application is about as simple as imaginable by simply giving you a dot on the screen to click on and then it generates a pop-up window for the duration of 5 seconds. The pop-up window is necessary for the ability of letting your mouse unhide a taskbar, if you have one hiding. For some reasons the initial dot taking focus from you clicking on it is not enough to work on its own, because it is a pinned application - pinned applications or always-on-top apps don't appear to be able to grab focus the same way as a regular app can. Regular apps with focus are enough to allow the autohide on the taskbar to work normally.
