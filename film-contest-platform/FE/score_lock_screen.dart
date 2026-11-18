import 'package:flutter/material.dart';
import '../models/score_lock_model.dart';

class ScoreLockScreen extends StatefulWidget {
  const ScoreLockScreen({super.key});

  @override
  State<ScoreLockScreen> createState() => _ScoreLockScreenState();
}

class _ScoreLockScreenState extends State<ScoreLockScreen> {
  final List<JudgeSubmissionScore> _items = [
    JudgeSubmissionScore(
      id: 'SUB-01',
      submissionTitle: 'Hoàng Hôn Cầu Thủ Thiêm (Frame #14)',
      contestantName: 'Nguyễn Minh Khôi',
      filmStock: 'Kodak Portra 400',
      imageUrl: 'https://picsum.photos/seed/lock1/600/400',
      score: 9.2,
      feedback: 'Ánh sáng và màu sắc tuyệt vời, bố cục chuẩn mực.',
      isConfirmed: true,
      isLocked: true, // Đã khóa cứng điểm
    ),
    JudgeSubmissionScore(
      id: 'SUB-02',
      submissionTitle: 'Gánh Hàng Rong Phố Cổ (Frame #07)',
      contestantName: 'Trần Thảo Vy',
      filmStock: 'Ilford HP5 Plus 400',
      imageUrl: 'https://picsum.photos/seed/lock2/600/400',
      score: 8.5,
      feedback: 'Độ tương phản đen trắng tốt, cảm xúc hoài niệm cao.',
      isConfirmed: false,
      isLocked: false, // Chưa khóa, giám khảo có thể sửa
    ),
  ];

  void _openScoreDialog(JudgeSubmissionScore item) {
    if (item.isLocked) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Bài này đã được xác nhận và khóa điểm, không thể chỉnh sửa!')),
      );
      return;
    }

    final scoreCtrl = TextEditingController(text: item.score.toString());
    final feedbackCtrl = TextEditingController(text: item.feedback);
    bool confirmLock = item.isConfirmed;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Padding(
              padding: EdgeInsets.only(
                left: 20,
                right: 20,
                top: 20,
                bottom: MediaQuery.of(context).viewInsets.bottom + 20,
              ),
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Chấm Điểm & Xác Nhận (${item.id})',
                          style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                        ),
                        IconButton(
                          icon: const Icon(Icons.close),
                          onPressed: () => Navigator.pop(ctx),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: Image.network(item.imageUrl, height: 160, width: double.infinity, fit: BoxFit.cover),
                    ),
                    const SizedBox(height: 12),
                    Text(item.submissionTitle, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                    Text('Tác giả: ${item.contestantName} • Film: ${item.filmStock}', style: TextStyle(color: Colors.grey.shade700, fontSize: 12)),
                    const SizedBox(height: 16),
                    TextField(
                      controller: scoreCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'Điểm số (Thang điểm 10)',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: feedbackCtrl,
                      maxLines: 2,
                      decoration: const InputDecoration(
                        labelText: 'Nhận xét của Giám khảo',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Switch xác nhận & khóa điểm (SRS FR-10.5)
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade50,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: Colors.amber.shade300),
                      ),
                      child: SwitchListTile(
                        contentPadding: EdgeInsets.zero,
                        title: const Text(
                          'Giám khảo xác nhận & Khóa điểm',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                        ),
                        subtitle: const Text(
                          'Sau khi xác nhận, điểm sẽ bị khóa và không thể thay đổi.',
                          style: TextStyle(fontSize: 12),
                        ),
                        activeColor: Colors.amber.shade800,
                        value: confirmLock,
                        onChanged: (val) => setModalState(() => confirmLock = val),
                      ),
                    ),
                    const SizedBox(height: 18),
                    SizedBox(
                      width: double.infinity,
                      height: 46,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.amber.shade800,
                          foregroundColor: Colors.white,
                        ),
                        onPressed: () {
                          setState(() {
                            item.score = double.tryParse(scoreCtrl.text) ?? item.score;
                            item.feedback = feedbackCtrl.text.trim();
                            item.isConfirmed = confirmLock;
                            item.isLocked = confirmLock; // Khóa điểm
                          });
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(confirmLock
                                  ? 'Đã xác nhận và khóa điểm bài "${item.submissionTitle}" thành công!'
                                  : 'Đã lưu nháp điểm số thành công!'),
                            ),
                          );
                        },
                        child: Text(confirmLock ? 'Xác Nhận & Khóa Điểm' : 'Lưu Nháp'),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F6F8),
      appBar: AppBar(
        title: const Text('Xác Nhận & Khóa Điểm Giám Khảo (FE10)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _items.length,
        itemBuilder: (context, index) {
          final item = _items[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 14),
            elevation: 2,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: InkWell(
              borderRadius: BorderRadius.circular(12),
              onTap: () => _openScoreDialog(item),
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(item.id, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey)),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: item.isLocked ? Colors.red.shade50 : Colors.amber.shade50,
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(color: item.isLocked ? Colors.red.shade300 : Colors.amber.shade400),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                item.isLocked ? Icons.lock : Icons.lock_open,
                                size: 13,
                                color: item.isLocked ? Colors.red.shade700 : Colors.amber.shade900,
                              ),
                              const SizedBox(width: 4),
                              Text(
                                item.isLocked ? 'Đã khóa điểm' : 'Chưa khóa (Đang chấm)',
                                style: TextStyle(
                                  color: item.isLocked ? Colors.red.shade700 : Colors.amber.shade900,
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(item.imageUrl, width: 75, height: 65, fit: BoxFit.cover),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(item.submissionTitle, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                              const SizedBox(height: 2),
                              Text('Tác giả: ${item.contestantName}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                              const SizedBox(height: 6),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: Colors.amber.shade100,
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text('Điểm: ${item.score}/10', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber.shade900)),
                                  ),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      item.feedback.isNotEmpty ? item.feedback : 'Chưa có nhận xét',
                                      style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontStyle: FontStyle.italic),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
