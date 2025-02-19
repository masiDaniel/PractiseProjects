import 'package:flutter/material.dart';
import 'package:neflix_frontend/screens/page_two.dart';
import 'package:neflix_frontend/screens/settings_page.dart';

class PageOne extends StatelessWidget {
  const PageOne({super.key});

  @override
  Widget build(BuildContext context) {
    // You can also add theme toggle functionality in PageOne if needed
    return Scaffold(
      appBar: AppBar(title: const Text('Page One')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('This is Page One!'),
            ElevatedButton(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const PageTwo()),
              ),
              child: const Text('Go to Page Two'),
            ),
            const SizedBox(height: 20),
            // Instead of duplicating toggle logic, you could also navigate to settings:
            ElevatedButton(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => SettingsPage(
                    // Obtain the toggle function from an InheritedWidget or Provider
                    // if you need it here. For simplicity, this example only
                    // passes it from HomePage.
                    toggleTheme: () {},
                  ),
                ),
              ),
              child: const Text('Go to Settings'),
            ),
          ],
        ),
      ),
    );
  }
}
