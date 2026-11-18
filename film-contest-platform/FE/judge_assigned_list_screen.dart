import 'package:flutter/material.dart';
import '../models/assigned_submission_model.dart';

class JudgeAssignedListScreen extends StatefulWidget {
  const JudgeAssignedListScreen({super.key});

  @override
  State<JudgeAssignedListScreen> createState() => _JudgeAssignedListScreenState();
}

class _JudgeAssignedListScreenState extends State<JudgeAssignedListScreen> {
  String _selectedFilter = 'Tất cả';

  final List<AssignedSubmission> _items = [
    AssignedSubmission(
      id: 'SUB-01',
      submissionTitle: 'Hoàng Hôn Cầu Thủ Thiêm (Frame #14)',
      contestantName: 'Nguyễn Minh Khôi',
      contestName: 'Nét Đẹp Đô Thị Việt Nam 2026',
      filmStock: 'Kodak Portra 400',
      iso: 400,
      shutterSpeed: '1/250s',
      aperture: 'f/2.8',
      location: 'Quận 2, TP.HCM',
      imageUrl: 'https://picsum.photos/seed/judge1/800/600',
      submittedAt: DateTime(2026, 11, 16, 14, 30),
      score: 9.2,
      status: 'Đã hoàn thành',
      feedback: 'Ánh sáng và màu sắc tuyệt vời, tái hiện chất film chân thực.',
    ),
    AssignedSubmission(
      id: 'SUB-02',
      submissionTitle: 'Gánh Hàng Rong Phố Cổ (Frame #07)',
      contestantName: 'Trần Thảo Vy',
      contestName: 'Khoảnh Khắc Đen Trắng & Hoài Niệm',
      filmStock: 'Ilford HP5 Plus 400',
      iso: 400,
      shutterSpeed: '1/500s',
      aperture: 'f/4.0',
      location: 'Quận 1, TP.HCM',
      imageUrl: 'https://picsum.photos/seed/judge2/800/600',
      submittedAt: DateTime(2026, 11, 17, 9, 15),
      score: 0.0,
      status: 'Chưa chấm',
      feedback: '',
    ),
  ];

  List<AssignedSubmission> get _filteredItems {
    if (_selectedFilter == 'Chưa chấm') {
      return _items.where((e) => e.status == 'Chưa chấm').toList();
    } else if (_selectedFilter == 'Đã hoàn thành') {
      return _items.where((e) => e.status == 'Đã hoàn thành').toList();
    }
    return _items;
  }

  int get _completedCount => _items.where((e) => e.status == 'Đã hoàn thành').length;
  double get _progress => _items.isEmpty ? 0 : _completedCount / _items.length;

  void _openDetailAndGrading(AssignedSubmission item) {
    final scoreCtrl = TextEditingController(text: item.score > 0 ? item.score.toString() : '');
    final feedbackCtrl = TextEditingController(text: item.feedback);

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Padding(
          padding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 18,
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
                      'Chấm Bài & Xem Metadata (${item.id})',
                      style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: () => Navigator.pop(ctx),
                    ),
                  ],
                ),
                const SizedBox(height: 8),

                // Ảnh phóng to (Zoomable Image preview)
                GestureDetector(
                  onTap: () {
                    // Mở popup xem ảnh full size phóng to
                    showDialog(
                      context: context,
                      builder: (_) => Dialog(
                        backgroundColor: Colors.black,
                        child: InteractiveViewer(
                          child: Image.network(item.imageUrl, fit: BoxFit.contain),
                        ),
                      ),
                    );
                  },
                  child: Stack(
                    alignment: Alignment.bottomRight,
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.network(item.imageUrl, height: 210, width: double.infinity, fit: BoxFit.cover),
                      ),
                      Container(
                        margin: const EdgeInsets.all(8),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: Colors.black54,
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.zoom_in, color: Colors.white, size: 16),
                            SizedBox(width: 4),
                            Text('Chạm để phóng to ảnh', style: TextStyle(color: Colors.white, fontSize: 11)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),

                Text(item.submissionTitle, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                Text('Tác giả: ${item.contestantName} • Cuộc thi: ${item.contestName}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                const SizedBox(height: 12),

                // Metadata Film chi tiết (SRS FR-10.2)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade50,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.amber.shade300),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.camera_roll, size: 16, color: Colors.amber),
                          SizedBox(width: 6),
                          Text('Thông số Metadata Phim & Chụp:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text('• Loại Film (Film Stock): ${item.filmStock} (ISO ${item.iso})', style: const TextStyle(fontSize: 12)),
                      Text('• Tốc độ màn trập: ${item.shutterSpeed} • Khẩu độ: ${item.aperture}', style: const TextStyle(fontSize: 12)),
                      Text('• Địa điểm: ${item.location}', style: const TextStyle(fontSize: 12)),
                    ],
                  ),
                ),
                const SizedBox(height: 14),

                TextField(
                  controller: scoreCtrl,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Điểm số (Thang điểm 10)',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: feedbackCtrl,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Nhận xét của Giám khảo',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),

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
                        item.score = double.tryParse(scoreCtrl.text) ?? item.score;
                        item.feedback = feedbackCtrl.text.trim();
                        item.status = 'Đã hoàn thành';
                      });
                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Đã lưu kết quả chấm bài "${item.submissionTitle}"!')),
                      );
                    },
                    child: const Text('Lưu & Hoàn Thành Chấm Bài'),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final filters = ['Tất cả', 'Chưa chấm', 'Đã hoàn thành'];

    return Scaffold(
      backgroundColor: const Color(0xFFF6F5F2),
      appBar: AppBar(
        title: const Text('Bài Được Giao & Chấm Điểm (FE10)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          // Banner Tiến độ chấm điểm (Progress tracking)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: const Color(0xFF222222),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Tiến độ chấm bài của bạn:', style: TextStyle(color: Colors.white70, fontSize: 13)),
                    Text('Đã xong: $_completedCount/${_items.length} bài', style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold)),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(6),
                  child: LinearProgressIndicator(
                    value: _progress,
                    minHeight: 8,
                    backgroundColor: Colors.white24,
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.amber.shade700),
                  ),
                ),
              ],
            ),
          ),

          // Thanh lọc trạng thái
          Container(
            height: 54,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: filters.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final f = filters[index];
                final isSelected = _selectedFilter == f;
                return ChoiceChip(
                  label: Text(f),
                  selected: isSelected,
                  selectedColor: Colors.amber.shade800,
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.white : Colors.black87,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  onSelected: (_) => setState(() => _selectedFilter = f),
                );
              },
            ),
          ),

          // Danh sách bài được giao
          Expanded(
            child: _filteredItems.isEmpty
                ? const Center(child: Text('Không có bài dự thi nào trong mục này.'))
                : ListView.builder(
                    padding: const EdgeInsets.all(14),
                    itemCount: _filteredItems.length,
                    itemBuilder: (context, index) {
                      final item = _filteredItems[index];
                      final isDone = item.status == 'Đã hoàn thành';

                      return Card(
                        margin: const EdgeInsets.only(bottom: 14),
                        elevation: 2,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(12),
                          onTap: () => _openDetailAndGrading(item),
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
                                        color: isDone ? Colors.green.shade50 : Colors.orange.shade50,
                                        borderRadius: BorderRadius.circular(6),
                                        border: Border.all(color: isDone ? Colors.green.shade300 : Colors.orange.shade300),
                                      ),
                                      child: Text(
                                        item.status,
                                        style: TextStyle(
                                          color: isDone ? Colors.green.shade700 : Colors.orange.shade800,
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                        ),
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
                                      child: Image.network(item.imageUrl, width: 85, height: 75, fit: BoxFit.cover),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            item.submissionTitle,
                                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                                            maxLines: 1,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                          const SizedBox(height: 3),
                                          Text('Tác giả: ${item.contestantName}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                                          Text('Film: ${item.filmStock} • ISO ${item.iso}', style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
                                          const SizedBox(height: 6),
                                          Row(
                                            children: [
                                              Container(
                                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                                decoration: BoxDecoration(
                                                  color: Colors.amber.shade100,
                                                  borderRadius: BorderRadius.circular(4),
                                                ),
                                                child: Text(
                                                  isDone ? 'Điểm: ${item.score}/10' : 'Chưa chấm điểm',
                                                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber.shade900),
                                                ),
                                              ),
                                              const Spacer(),
                                              const Icon(Icons.zoom_out_map, size: 14, color: Colors.grey),
                                              const SizedBox(width: 4),
                                              const Text('Xem & Phóng to', style: TextStyle(fontSize: 11, color: Colors.grey)),
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
          ),
        ],
      ),
    );
  }
}
