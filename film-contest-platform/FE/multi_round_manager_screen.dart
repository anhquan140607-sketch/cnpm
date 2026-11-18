import 'package:flutter/material.dart';
import '../models/round_model.dart';

class MultiRoundManagerScreen extends StatefulWidget {
  const MultiRoundManagerScreen({super.key});

  @override
  State<MultiRoundManagerScreen> createState() => _MultiRoundManagerScreenState();
}

class _MultiRoundManagerScreenState extends State<MultiRoundManagerScreen> {
  int _selectedRoundIndex = 0;

  late List<ContestRound> _rounds;

  @override
  void initState() {
    super.initState();
    _rounds = [
      ContestRound(
        id: 'ROUND-01',
        stage: ContestRoundStage.preliminary,
        roundName: 'Vòng Loại (Preliminary)',
        description: 'Chấm sơ loại toàn bộ ảnh nộp, lọc các bài hợp lệ vào Shortlist.',
        isCurrentActive: false,
        submissions: [
          SubmissionItem(id: 'SUB-01', title: 'Phố Cổ Sài Gòn', author: 'Nguyễn Minh Khôi', filmStock: 'Kodak Portra 400', imageUrl: 'https://picsum.photos/seed/r1_1/600/400', score: 8.5, isQualifiedToNextRound: true, roundStatus: 'Đã qua vòng'),
          SubmissionItem(id: 'SUB-02', title: 'Gánh Hàng Rong', author: 'Trần Thảo Vy', filmStock: 'Ilford HP5 400', imageUrl: 'https://picsum.photos/seed/r1_2/600/400', score: 7.2, isQualifiedToNextRound: true, roundStatus: 'Đã qua vòng'),
          SubmissionItem(id: 'SUB-03', title: 'Bến Nhà Rồng Chiều', author: 'Lê Hoàng Nam', filmStock: 'Fujifilm C200', imageUrl: 'https://picsum.photos/seed/r1_3/600/400', score: 5.1, isQualifiedToNextRound: false, roundStatus: 'Đã loại'),
        ],
      ),
      ContestRound(
        id: 'ROUND-02',
        stage: ContestRoundStage.shortlist,
        roundName: 'Vòng Shortlist (Top Chọn Lọc)',
        description: 'Chấm điểm chuyên sâu các bài đạt chuẩn vòng loại để chọn vào Chung kết.',
        isCurrentActive: true,
        submissions: [
          SubmissionItem(id: 'SUB-01', title: 'Phố Cổ Sài Gòn', author: 'Nguyễn Minh Khôi', filmStock: 'Kodak Portra 400', imageUrl: 'https://picsum.photos/seed/r1_1/600/400', score: 9.1, isQualifiedToNextRound: true, roundStatus: 'Vào Chung Kết'),
          SubmissionItem(id: 'SUB-02', title: 'Gánh Hàng Rong', author: 'Trần Thảo Vy', filmStock: 'Ilford HP5 400', imageUrl: 'https://picsum.photos/seed/r1_2/600/400', score: 8.4, isQualifiedToNextRound: true, roundStatus: 'Vào Chung Kết'),
        ],
      ),
      ContestRound(
        id: 'ROUND-03',
        stage: ContestRoundStage.finalRound,
        roundName: 'Vòng Chung Kết (Finals)',
        description: 'Xếp hạng huy chương và trao giải nhất, nhì, ba.',
        isCurrentActive: false,
        submissions: [
          SubmissionItem(id: 'SUB-01', title: 'Phố Cổ Sài Gòn', author: 'Nguyễn Minh Khôi', filmStock: 'Kodak Portra 400', imageUrl: 'https://picsum.photos/seed/r1_1/600/400', score: 9.4, isQualifiedToNextRound: true, roundStatus: 'Đạt Giải Nhì'),
        ],
      ),
    ];
  }

  void _showScoreAndPromoteDialog(SubmissionItem sub, ContestRound currentRound) {
    final scoreController = TextEditingController(text: sub.score.toString());
    bool qualified = sub.isQualifiedToNextRound;

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
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Chấm Điểm & Đẩy Vòng: ${sub.title}',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  Text('Tác giả: ${sub.author} • ${currentRound.roundName}', style: const TextStyle(color: Colors.grey)),
                  const SizedBox(height: 16),
                  TextField(
                    controller: scoreController,
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    decoration: const InputDecoration(
                      labelText: 'Điểm số vòng này (Thang điểm 10)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 14),
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('Chọn bài vào vòng sau / Shortlist'),
                    subtitle: const Text('Đưa tác phẩm này tiếp tục tranh tài ở vòng kế tiếp'),
                    activeColor: Colors.amber.shade800,
                    value: qualified,
                    onChanged: (val) => setModalState(() => qualified = val),
                  ),
                  const SizedBox(height: 18),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.amber.shade800,
                        foregroundColor: Colors.white,
                      ),
                      onPressed: () {
                        setState(() {
                          sub.score = double.tryParse(scoreController.text) ?? sub.score;
                          sub.isQualifiedToNextRound = qualified;
                          sub.roundStatus = qualified ? 'Đã qua vòng / Shortlist' : 'Đã loại';
                        });
                        Navigator.pop(ctx);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Đã cập nhật kết quả cho "${sub.title}"!')),
                        );
                      },
                      child: const Text('Lưu & Cập Nhật Trạng Thái'),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final currentRound = _rounds[_selectedRoundIndex];

    return Scaffold(
      backgroundColor: const Color(0xFFF6F5F2),
      appBar: AppBar(
        title: const Text('Cấu Hình & Quản Lý Nhiều Vòng Chấm (FE10)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          // Thanh chọn vòng chấm (Tabs)
          Container(
            height: 60,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: _rounds.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final r = _rounds[index];
                final isSelected = _selectedRoundIndex == index;
                return ChoiceChip(
                  label: Text(r.roundName),
                  selected: isSelected,
                  selectedColor: Colors.amber.shade800,
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.white : Colors.black87,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  onSelected: (_) => setState(() => _selectedRoundIndex = index),
                );
              },
            ),
          ),

          // Mô tả vòng chấm hiện tại
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(14),
            margin: const EdgeInsets.symmetric(horizontal: 14),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.amber.shade200),
            ),
            child: Row(
              children: [
                Icon(Icons.rule_folder, color: Colors.amber.shade800, size: 28),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(currentRound.roundName, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      const SizedBox(height: 2),
                      Text(currentRound.description, style: TextStyle(color: Colors.grey.shade700, fontSize: 12)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),

          // Danh sách bài dự thi trong vòng chấm
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              itemCount: currentRound.submissions.length,
              itemBuilder: (context, index) {
                final sub = currentRound.submissions[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(12),
                    leading: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(sub.imageUrl, width: 70, height: 60, fit: BoxFit.cover),
                    ),
                    title: Text(sub.title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 2),
                        Text('Tác giả: ${sub.author} • Film: ${sub.filmStock}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                        const SizedBox(height: 6),
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: Colors.amber.shade100,
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text('Điểm: ${sub.score}/10', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber.shade900)),
                            ),
                            const SizedBox(width: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: sub.isQualifiedToNextRound ? Colors.teal.shade50 : Colors.red.shade50,
                                borderRadius: BorderRadius.circular(4),
                                border: Border.all(color: sub.isQualifiedToNextRound ? Colors.teal.shade300 : Colors.red.shade300),
                              ),
                              child: Text(
                                sub.roundStatus,
                                style: TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                  color: sub.isQualifiedToNextRound ? Colors.teal.shade700 : Colors.red.shade700,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.edit_note, color: Colors.amber, size: 28),
                      onPressed: () => _showScoreAndPromoteDialog(sub, currentRound),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
