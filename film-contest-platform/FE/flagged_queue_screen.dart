import 'package:flutter/material.dart';
import '../models/flagged_submission_model.dart';

class FlaggedQueueScreen extends StatefulWidget {
  const FlaggedQueueScreen({super.key});

  @override
  State<FlaggedQueueScreen> createState() => _FlaggedQueueScreenState();
}

class _FlaggedQueueScreenState extends State<FlaggedQueueScreen> {
  String _selectedFilter = 'Chờ xử lý';

  final List<FlaggedSubmission> _flaggedItems = [
    FlaggedSubmission(
      id: 'FLAG-101',
      submissionTitle: 'Hoàng Hôn Cầu Thủ Thiêm (Frame #14)',
      contestantName: 'Nguyễn Minh Khôi',
      contestantEmail: 'khoi.nm@example.com',
      contestName: 'Nét Đẹp Đô Thị Việt Nam 2026',
      filmStock: 'Kodak Portra 400',
      imageUrl: 'https://picsum.photos/seed/flag101/700/450',
      flagReasons: [
        'AI Phát hiện vùng biên hạt (film grain) không đồng nhất - nghi vấn ghép trời bằng AI/Photoshop.',
        'Metadata file scan chứa chữ ký phần mềm Adobe Generative Fill.',
      ],
      aiAnomalyScore: 88.5,
      severity: FlagSeverity.high,
      flaggedAt: DateTime(2026, 11, 18, 21, 15),
      status: FlagStatus.pending,
    ),
    FlaggedSubmission(
      id: 'FLAG-102',
      submissionTitle: 'Gánh Hàng Rong Phố Cổ (Frame #07)',
      contestantName: 'Trần Thảo Vy',
      contestantEmail: 'vy.tt@example.com',
      contestName: 'Khoảnh Khắc Đen Trắng & Hoài Niệm',
      filmStock: 'Ilford HP5 Plus 400',
      imageUrl: 'https://picsum.photos/seed/flag102/700/450',
      flagReasons: [
        'Tỷ lệ khung hình 16:9 bất thường so với chuẩn phim 35mm (3:2).',
        'Thí sinh chưa đính kèm ảnh chụp dải âm bản (negative strip) đối chiếu.',
      ],
      aiAnomalyScore: 54.0,
      severity: FlagSeverity.medium,
      flaggedAt: DateTime(2026, 11, 18, 19, 40),
      status: FlagStatus.pending,
    ),
    FlaggedSubmission(
      id: 'FLAG-103',
      submissionTitle: 'Sớm Mai Trên Sông Hương (Frame #22)',
      contestantName: 'Lê Hoàng Nam',
      contestantEmail: 'nam.lh@example.com',
      contestName: 'Hơi Thở Thiên Nhiên & Con Người',
      filmStock: 'Fujifilm Superia X-Tra 400',
      imageUrl: 'https://picsum.photos/seed/flag103/700/450',
      flagReasons: [
        'Cảnh báo trùng lặp hash ảnh 72% với một tác phẩm đã nộp ở vòng loại tháng trước.',
      ],
      aiAnomalyScore: 31.2,
      severity: FlagSeverity.low,
      flaggedAt: DateTime(2026, 11, 17, 14, 10),
      status: FlagStatus.approved,
      moderatorNote: 'Đã đối chiếu negative gốc, góc chụp khác nhau ở thời điểm bấm máy.',
    ),
  ];

  List<FlaggedSubmission> get _filteredItems {
    if (_selectedFilter == 'Chờ xử lý') {
      return _flaggedItems.where((e) => e.status == FlagStatus.pending).toList();
    } else if (_selectedFilter == 'Đã gỡ cờ') {
      return _flaggedItems.where((e) => e.status == FlagStatus.approved).toList();
    } else if (_selectedFilter == 'Đã từ chối') {
      return _flaggedItems.where((e) => e.status == FlagStatus.rejected).toList();
    }
    return _flaggedItems;
  }

  Color _getSeverityColor(FlagSeverity severity) {
    switch (severity) {
      case FlagSeverity.high:
        return Colors.red.shade700;
      case FlagSeverity.medium:
        return Colors.orange.shade800;
      case FlagSeverity.low:
        return Colors.amber.shade700;
    }
  }

  String _getSeverityLabel(FlagSeverity severity) {
    switch (severity) {
      case FlagSeverity.high:
        return 'Nghi vấn cao';
      case FlagSeverity.medium:
        return 'Trung bình';
      case FlagSeverity.low:
        return 'Cảnh báo nhẹ';
    }
  }

  void _openReviewSheet(FlaggedSubmission item) {
    final noteController = TextEditingController(text: item.moderatorNote ?? '');

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
                      'Kiểm Duyệt Bài Gắn Cờ (${item.id})',
                      style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: () => Navigator.pop(ctx),
                    ),
                  ],
                ),
                const SizedBox(height: 8),

                // Ảnh bài dự thi bị gắn cờ
                ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    item.imageUrl,
                    height: 190,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                ),
                const SizedBox(height: 12),

                Text(
                  item.submissionTitle,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                Text(
                  'Thí sinh: ${item.contestantName} (${item.contestantEmail}) • Film: ${item.filmStock}',
                  style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
                ),
                const SizedBox(height: 14),

                // Danh sách lý do gắn cờ
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.flag, color: Colors.red.shade700, size: 18),
                          const SizedBox(width: 6),
                          Text(
                            'Lý do gắn cờ (Điểm bất thường AI: ${item.aiAnomalyScore}%):',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.red.shade900,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      ...item.flagReasons.map(
                        (reason) => Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('• ', style: TextStyle(fontWeight: FontWeight.bold)),
                              Expanded(
                                child: Text(reason, style: const TextStyle(fontSize: 13)),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),

                TextField(
                  controller: noteController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Ghi chú của Kiểm duyệt viên (Moderator Note)',
                    hintText: 'Nhập lý do gỡ cờ hoặc từ chối bài dự thi...',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),

                // Nút hành động: Gỡ cờ (Hợp lệ) / Từ chối (Vi phạm)
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.red.shade700,
                          side: BorderSide(color: Colors.red.shade400),
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                        onPressed: () {
                          setState(() {
                            item.status = FlagStatus.rejected;
                            item.moderatorNote = noteController.text.trim();
                          });
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Đã từ chối bài "${item.submissionTitle}" do vi phạm.')),
                          );
                        },
                        icon: const Icon(Icons.block),
                        label: const Text('Từ Chối Bài'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.teal.shade700,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                        onPressed: () {
                          setState(() {
                            item.status = FlagStatus.approved;
                            item.moderatorNote = noteController.text.trim();
                          });
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Đã gỡ cờ & chấp nhận bài "${item.submissionTitle}".')),
                          );
                        },
                        icon: const Icon(Icons.check_circle_outline),
                        label: const Text('Gỡ Cờ (Hợp Lệ)'),
                      ),
                    ),
                  ],
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
    final filters = ['Chờ xử lý', 'Tất cả', 'Đã gỡ cờ', 'Đã từ chối'];

    return Scaffold(
      backgroundColor: const Color(0xFFF5F6F8),
      appBar: AppBar(
        title: const Text('Hàng Đợi Bài Bị Gắn Cờ (FE8)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          // Thanh lọc trạng thái hàng đợi
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
                  selectedColor: Colors.red.shade700,
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.white : Colors.black87,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  onSelected: (_) => setState(() => _selectedFilter = f),
                );
              },
            ),
          ),

          // Danh sách bài nghi vấn kèm lý do gắn cờ
          Expanded(
            child: _filteredItems.isEmpty
                ? const Center(child: Text('Không có bài dự thi nào trong mục này.'))
                : ListView.builder(
                    padding: const EdgeInsets.all(14),
                    itemCount: _filteredItems.length,
                    itemBuilder: (context, index) {
                      final item = _filteredItems[index];
                      final sevColor = _getSeverityColor(item.severity);

                      return Card(
                        margin: const EdgeInsets.only(bottom: 14),
                        elevation: 2,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(12),
                          onTap: () => _openReviewSheet(item),
                          child: Padding(
                            padding: const EdgeInsets.all(14),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Header: Mã cờ + Mức độ nghi vấn
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(Icons.flag_rounded, color: sevColor, size: 18),
                                        const SizedBox(width: 6),
                                        Text(
                                          item.id,
                                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                        ),
                                      ],
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                      decoration: BoxDecoration(
                                        color: sevColor.withOpacity(0.12),
                                        borderRadius: BorderRadius.circular(6),
                                        border: Border.all(color: sevColor.withOpacity(0.5)),
                                      ),
                                      child: Text(
                                        '${_getSeverityLabel(item.severity)} (${item.aiAnomalyScore}%)',
                                        style: TextStyle(
                                          color: sevColor,
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),

                                // Thumbnail + Thông tin bài dự thi
                                Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    ClipRRect(
                                      borderRadius: BorderRadius.circular(8),
                                      child: Image.network(
                                        item.imageUrl,
                                        width: 84,
                                        height: 68,
                                        fit: BoxFit.cover,
                                      ),
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
                                          Text(
                                            'Thí sinh: ${item.contestantName}',
                                            style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
                                          ),
                                          Text(
                                            'Cuộc thi: ${item.contestName}',
                                            style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                                            maxLines: 1,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),

                                // Box hiển thị lý do gắn cờ nổi bật
                                Container(
                                  width: double.infinity,
                                  padding: const EdgeInsets.all(10),
                                  decoration: BoxDecoration(
                                    color: Colors.red.shade50.withOpacity(0.7),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Row(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Icon(Icons.warning_amber_rounded, size: 16, color: Colors.red.shade700),
                                      const SizedBox(width: 6),
                                      Expanded(
                                        child: Text(
                                          'Lý do: ${item.flagReasons.first}',
                                          style: TextStyle(fontSize: 12, color: Colors.red.shade900),
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                        ),
                                      ),
                                    ],
                                  ),
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
