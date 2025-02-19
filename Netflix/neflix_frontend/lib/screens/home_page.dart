import 'package:flutter/material.dart';
import 'package:neflix_frontend/screens/page_one.dart';
import 'package:neflix_frontend/screens/settings_page.dart';

class HomePage extends StatelessWidget {
  final VoidCallback toggleTheme;
  const HomePage({super.key, required this.toggleTheme});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home Page')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Welcome to Home Page!'),
            ElevatedButton(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const PageOne(),
                ),
              ),
              child: const Text('Go to Page One'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => SettingsPage(toggleTheme: toggleTheme),
                ),
              ),
              child: const Text('Go to Settings'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: toggleTheme,
              child: const Text('Toggle Theme'),
            ),
          ],
        ),
      ),
    );
  }
}
