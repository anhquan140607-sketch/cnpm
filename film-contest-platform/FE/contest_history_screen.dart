import 'package:flutter/material.dart';
import '../models/contest_history_model.dart';

class ContestHistoryScreen extends StatefulWidget {
  const ContestHistoryScreen({super.key});

  @override
  State<ContestHistoryScreen> createState() => _ContestHistoryScreenState();
}

class _ContestHistoryScreenState extends State<ContestHistoryScreen> {
  String _selectedFilter = 'Tất cả';

  final List<ContestHistoryItem> _historyList = [
    ContestHistoryItem(
      id: 'HIS-01',
      contestTitle: 'Nét Đẹp Đô Thị Việt Nam 2026',
      organizer: 'Film Club Sài Gòn',
      submissionTitle: 'Khung hình #03 - Phố cổ Sài Gòn',
      joinedDate: '10/11/2026',
      status: 'Đã kết thúc',
      isPublished: true, // Đã công bố kết quả
      score: 9.2,
      prize: 'Giải Nhì',
      judgeFeedback: 'Bố cục ánh sáng ấn tượng, tái hiện trọn vẹn hồn xưa qua lớp film Kodak Portra 400.',
    ),
    ContestHistoryItem(
      id: 'HIS-02',
      contestTitle: 'Khoảnh Khắc Đen Trắng & Hoài Niệm',
      organizer: 'Hội Nhiếp Ảnh Nghệ Thuật',
      submissionTitle: 'Khung hình #12 - Chợ Bến Thành',
      joinedDate: '15/11/2026',
      status: 'Đang diễn ra',
      isPublished: false, // Chưa công bố kết quả
      score: null,
      prize: null,
      judgeFeedback: null,
    ),
  ];

  List<ContestHistoryItem> get _filteredList {
    if (_selectedFilter == 'Đang diễn ra') {
      return _historyList.where((e) => !e.isPublished).toList();
    } else if (_selectedFilter == 'Đã hoàn thành & Có kết quả') {
      return _historyList.where((e) => e.isPublished).toList();
    }
    return _historyList;
  }

  void _showDetailDialog(ContestHistoryItem item) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      item.contestTitle,
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.grey),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Text(
                item.submissionTitle,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 6),
              Text('Đơn vị tổ chức: ${item.organizer} • Ngày tham gia: ${item.joinedDate}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
              const Divider(height: 24),

              if (!item.isPublished) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.orange.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.orange.shade200),
                  ),
                  child: const Row(
                    children: [
                      Icon(Icons.hourglass_top, color: Colors.orange, size: 20),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'Cuộc thi đang diễn ra hoặc chưa công bố kết quả chính thức.',
                          style: TextStyle(fontSize: 13, color: Colors.orange),
                        ),
                      ),
                    ],
                  ),
                ),
              ] else ...[
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade100,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        'Điểm số: ${item.score}/10',
                        style: TextStyle(fontWeight: FontWeight.bold, color: Colors.amber.shade900, fontSize: 15),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.indigo.shade50,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.indigo.shade200),
                      ),
                      child: Text(
                        item.prize ?? 'Không có giải',
                        style: TextStyle(fontWeight: FontWeight.bold, color: Colors.indigo.shade700, fontSize: 14),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                const Text('Nhận xét từ Giám khảo:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                const SizedBox(height: 6),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    item.judgeFeedback ?? 'Chưa có nhận xét.',
                    style: const TextStyle(fontStyle: FontStyle.italic, fontSize: 13),
                  ),
                ),
              ],
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                height: 46,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF1E1E1E),
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('Đóng'),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final filters = ['Tất cả', 'Đang diễn ra', 'Đã hoàn thành & Có kết quả'];

    return Scaffold(
      backgroundColor: const Color(0xFFF6F5F2),
      appBar: AppBar(
        title: const Text('Lịch Sử Cuộc Thi Của Thí Sinh (FE5)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
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
          Expanded(
            child: _filteredList.isEmpty
                ? const Center(child: Text('Không có lịch sử cuộc thi nào trong mục này.'))
                : ListView.builder(
                    padding: const EdgeInsets.all(14),
                    itemCount: _filteredList.length,
                    itemBuilder: (context, index) {
                      final item = _filteredList[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 14),
                        elevation: 2,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(12),
                          onTap: () => _showDetailDialog(item),
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
                                        item.contestTitle,
                                        style: const TextStyle(fontSize: 13, color: Colors.grey, fontWeight: FontWeight.bold),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                      decoration: BoxDecoration(
                                        color: item.isPublished ? Colors.green.shade50 : Colors.orange.shade50,
                                        borderRadius: BorderRadius.circular(6),
                                        border: Border.all(
                                          color: item.isPublished ? Colors.green.shade300 : Colors.orange.shade300,
                                        ),
                                      ),
                                      child: Text(
                                        item.isPublished ? 'Đã có kết quả' : 'Đang diễn ra',
                                        style: TextStyle(
                                          color: item.isPublished ? Colors.green.shade700 : Colors.orange.shade800,
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  item.submissionTitle,
                                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  children: [
                                    const Icon(Icons.calendar_today, size: 14, color: Colors.grey),
                                    const SizedBox(width: 6),
                                    Text('Ngày tham gia: ${item.joinedDate}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                                  ],
                                ),
                                if (item.isPublished) ...[
                                  const SizedBox(height: 10),
                                  Row(
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                        decoration: BoxDecoration(
                                          color: Colors.amber.shade100,
                                          borderRadius: BorderRadius.circular(4),
                                        ),
                                        child: Text(
                                          'Điểm: ${item.score}/10',
                                          style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber.shade900),
                                        ),
                                      ),
                                      const SizedBox(width: 8),
                                      Text(
                                        item.prize ?? '',
                                        style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.indigo.shade700),
                                      ),
                                      const Spacer(),
                                      const Icon(Icons.chevron_right, color: Colors.grey),
                                    ],
                                  ),
                                ],
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
