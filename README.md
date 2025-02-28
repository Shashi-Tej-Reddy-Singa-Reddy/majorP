# majorP
hello
hello
1. Geometric Transformations
These change the spatial structure of the image while preserving content.

Rotation: Rotating images by a certain degree (e.g., ±90° or random rotations).
Scaling: Resizing images while maintaining aspect ratio.
Translation: Shifting images horizontally or vertically.
Shearing: Distorting the image along the x- or y-axis.
Flipping: Mirroring images horizontally or vertically.
Cropping: Extracting a region of interest from the image.
Padding: Adding extra pixels around the image.
2. Color Space Transformations
These alter the colors to make models robust to lighting and contrast variations.

Brightness Adjustment: Increasing or decreasing brightness.
Contrast Adjustment: Enhancing or reducing contrast.
Saturation Adjustment: Modifying color intensity.
Hue Shift: Changing color tones.
Grayscale Conversion: Converting colored images to grayscale.
Color Jittering: Randomly altering brightness, contrast, saturation, and hue.
3. Noise Injection & Blurring
Adding noise makes models more robust to real-world variations.

Gaussian Noise: Adding random noise to simulate sensor noise.
Salt-and-Pepper Noise: Introducing random black and white pixels.
Speckle Noise: Common in medical imaging.
Motion Blur: Simulating the effect of motion.
Gaussian Blur: Softening the image.
4. Occlusion & Erasure Techniques
Used for robustness against missing or occluded data.

Cutout: Removing random rectangular patches from the image.
Mixup: Combining two images by blending pixel values.
CutMix: Cutting a region from one image and pasting it into another.
Random Erasing: Erasing small patches in an image to simulate occlusions.
5. Style Transfer & Domain Adaptation
Used in deep learning to handle domain shift problems.

Histogram Matching: Matching color histograms of different images.
GAN-based Augmentation: Using Generative Adversarial Networks (GANs) to generate new images.
Style Transfer: Applying artistic or domain-specific styles to images