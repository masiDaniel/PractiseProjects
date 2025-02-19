import 'dart:ui';
import 'package:flutter/material.dart';

class PageTwo extends StatelessWidget {
  const PageTwo({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Page Two')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Fixed container for the image and blur overlay
            Container(
              height: 500,
              width: double.infinity,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  // Background image fills the container
                  Image.asset(
                    'assets/images/netflix_logo.png',
                    fit: BoxFit.fill,
                  ),
                  // Blurred overlay positioned at the bottom
                  Positioned(
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: ClipRect(
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
                        child: Container(
                          height: 150,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              colors: [
                                Colors.transparent,
                                const Color.fromARGB(255, 252, 2, 2)
                                    .withOpacity(0.5),
                              ],
                            ),
                          ),
                          alignment: Alignment.center,
                          child: Column(
                            children: [
                              const Text(
                                'Get ready tp dive into the greatest stories in TV and Film',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                ),
                              ),
                              const Text(
                                'Your Blurred Text Here',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                ),
                              ),
                              const Text(
                                'Your Blurred Text Here',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Back to Previous Page'),
            ),
          ],
        ),
      ),
    );
  }
}
