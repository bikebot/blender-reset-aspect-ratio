# blender-reset-aspect-ratio
A Blender plugin to reset the aspect ratio of image and video strips in the VSE

By default, Blender VSE scales images to fill both the x and y dimensions of render output dimensions. If the aspect ratio of the image/video does not match the render dimensions, images/videos are distorted. With this plugin, you can correct the aspect ratio of the image/video strip at a push of a button. 

The plugin adds two items to the Transform effect strip (in the Effect strip panel):
 * A Reset Aspect Ratio button
 * A Fit Scale slider: scales the image/video while keeping aspect ratio
 
To use the plugin, add a Transform effect strip to your image/video strip or to a group of strips and press the Reset Aspect Ratio button in the Effect Strip panel.
