import 'package:flutter/material.dart';

class ContestModel {
  final String id;
  final String title;
  final String organizer;
  final String deadline;
  final String prize;
  bool isRegistered;

  ContestModel({
    required this.id,
    required this.title,
    required this.organizer,
    required this.deadline,
    required this.prize,
    this.isRegistered = false,
  });
}

class ContestListScreen extends StatefulWidget {
  const ContestListScreen({super.key});

  @override
  State<ContestListScreen> createState() => _ContestListScreenState();
}

class _ContestListScreenState extends State<ContestListScreen> {
  final List<ContestModel> _contests = [
    ContestModel(
      id: 'C-01',
      title: 'Nét Đẹp Đô Thị Việt Nam 2026',
      organizer: Thí sinh Film Club Sài Gòn',
      deadline: '30/11/2026',
      prize: 'Giải Nhất: 20.000.000 VNĐ + 1 Cuộn Kodak Portra 400',
      isRegistered: true,
    ),
    ContestModel(
      id: 'C-02',
      title: 'Khoảnh Khắc Đen Trắng & Hoài Niệm',
      organizer: Hội Nhiếp Ảnh Nghệ Thuật',
      deadline: '15/12/2026',
      prize: 'Giải Nhất: 15.000.000 VNĐ',
      isRegistered: false,
    ),
    ContestModel(
      id: 'C-03',
      title: 'Hơi Thở Thiên Nhiên & Con Người',
      organizer: National Geographic VN',
      deadline: '31/12/2026',
      prize: 'Giải Đặc Biệt: 30.000.000 VNĐ',
      isRegistered: false,
    ),
  ];

  void _toggleRegister(ContestModel contest) {
    setState(() {
      contest.isRegistered = !contest.isRegistered;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(contest.isRegistered
            ? 'Đăng ký thành công cuộc thi "${contest.title}"!'
            : 'Đã hủy đăng ký cuộc thi "${contest.title}".'),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Danh Sách Cuộc Thi Film Photography'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _contests.length,
        itemBuilder: (context, index) {
          final contest = _contests[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            elevation: 2,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Text(
                          contest.title,
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: contest.isRegistered ? Colors.teal.shade50 : Colors.amber.shade50,
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(
                            color: contest.isRegistered ? Colors.teal : Colors.amber.shade800,
                          ),
                        ),
                        child: Text(
                          contest.isRegistered ? 'Đã tham gia' : 'Sắp diễn ra',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: contest.isRegistered ? Colors.teal.shade700 : Colors.amber.shade900,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.business, size: 15, color: Colors.grey),
                      const SizedBox(width: 6),
                      Text('Đơn vị: ${contest.organizer}', style: const TextStyle(fontSize: 13, color: Colors.grey)),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(Icons.card_giftcard, size: 15, color: Colors.orange),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(contest.prize, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(Icons.timer_outlined, size: 15, color: Colors.redAccent),
                      const SizedBox(width: 6),
                      Text('Hạn nộp: ${contest.deadline}', style: const TextStyle(fontSize: 13, color: Colors.redAccent, fontWeight: FontWeight.w500)),
                    ],
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    height: 40,
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: contest.isRegistered ? Colors.red.shade700 : Colors.amber.shade900,
                        side: BorderSide(color: contest.isRegistered ? Colors.red.shade300 : Colors.amber.shade800),
                      ),
                      onPressed: () => _toggleRegister(contest),
                      icon: Icon(contest.isRegistered ? Icons.cancel_outlined : Icons.how_to_reg),
                      label: Text(contest.isRegistered ? 'Hủy đăng ký cuộc thi' : 'Đăng ký tham gia ngay'),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
