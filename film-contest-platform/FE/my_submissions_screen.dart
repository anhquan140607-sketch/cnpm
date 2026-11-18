import 'package:flutter/material.dart';

class MySubmissionsScreen extends StatelessWidget {
  const MySubmissionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final submissions = [
      {'title': 'Khung hình #03 - Phố cổ Sài Gòn', 'contest': 'Nét Đẹp Đô Thị 2026', 'status': 'Đã duyệt', 'date': '12/11/2026'},
      {'title': 'Khung hình #12 - Chợ Bến Thành', 'contest': 'Nét Đẹp Đô Thị 2026', 'status': 'Đang chấm', 'date': '12/11/2026'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Bài Dự Thi Của Tôi'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: submissions.length,
        itemBuilder: (context, index) {
          final sub = submissions[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: const Icon(Icons.image, size: 40, color: Colors.amber),
              title: Text(sub['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Cuộc thi: ${sub['contest']}\nNgày nộp: ${sub['date']}'),
              isThreeLine: true,
              trailing: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: sub['status'] == 'Đã duyệt' ? Colors.green.shade50 : Colors.orange.shade50,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  sub['status']!,
                  style: TextStyle(
                    color: sub['status'] == 'Đã duyệt' ? Colors.green.shade700 : Colors.orange.shade800,
                    fontWeight: FontWeight.bold,
                    fontSize: 12,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
