import 'package:flutter/material.dart';
import '../models/submission_model.dart';

class SubmissionManagerScreen extends StatefulWidget {
  const SubmissionManagerScreen({super.key});

  @override
  State<SubmissionManagerScreen> createState() => _SubmissionManagerScreenState();
}

class _SubmissionManagerScreenState extends State<SubmissionManagerScreen> {
  final List<ContestSubmission> _submissions = [
    ContestSubmission(
      id: 'SUB-01',
      contestTitle: 'Nét Đẹp Đô Thị Việt Nam 2026',
      imagePath: 'https://picsum.photos/seed/sub1/600/400',
      title: 'Khung hình #03 - Phố cổ Sài Gòn',
      filmStock: 'Kodak Portra 400',
      iso: 400,
      shutterSpeed: '1/250s',
      aperture: 'f/2.8',
      location: 'Quận 1, TP.HCM',
      status: 'Đã duyệt',
      submittedAt: DateTime(2026, 11, 12, 10, 30),
    ),
    ContestSubmission(
      id: 'SUB-02',
      contestTitle: 'Khoảnh Khắc Đen Trắng & Hoài Niệm',
      imagePath: 'https://picsum.photos/seed/sub2/600/400',
      title: 'Khung hình #12 - Chợ Bến Thành',
      filmStock: 'Ilford HP5 Plus 400',
      iso: 400,
      shutterSpeed: '1/500s',
      aperture: 'f/4.0',
      location: 'Quận 1, TP.HCM',
      status: 'Đang chấm',
      submittedAt: DateTime(2026, 11, 15, 14, 20),
    ),
  ];

  void _showAddOrEditDialog({ContestSubmission? editItem}) {
    final titleCtrl = TextEditingController(text: editItem?.title ?? '');
    final stockCtrl = TextEditingController(text: editItem?.filmStock ?? 'Kodak Gold 200');
    final shutterCtrl = TextEditingController(text: editItem?.shutterSpeed ?? '1/250s');
    final apertureCtrl = TextEditingController(text: editItem?.aperture ?? 'f/4.0');
    final locationCtrl = TextEditingController(text: editItem?.location ?? 'TP. Hồ Chí Minh');
    int selectedIso = editItem?.iso ?? 200;
    String selectedContest = editItem?.contestTitle ?? 'Nét Đẹp Đô Thị Việt Nam 2026';
    String imagePreview = editItem?.imagePath ?? 'https://picsum.photos/seed/new_sub/600/400';

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
                          editItem == null ? 'Nộp Ảnh & Nhập Metadata' : 'Chỉnh Sửa Bài Dự Thi',
                          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        IconButton(
                          icon: const Icon(Icons.close),
                          onPressed: () => Navigator.pop(ctx),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),

                    // Chọn ảnh / Preview ảnh
                    Container(
                      height: 160,
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: Colors.black87,
                        borderRadius: BorderRadius.circular(12),
                        image: DecorationImage(
                          image: NetworkImage(imagePreview),
                          fit: BoxFit.cover,
                        ),
                      ),
                      child: Center(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.black54, foregroundColor: Colors.white),
                          onPressed: () {
                            setModalState(() {
                              imagePreview = 'https://picsum.photos/seed/random_${DateTime.now().millisecond}/600/400';
                            });
                          },
                          icon: const Icon(Icons.add_a_photo),
                          label: const Text('Chọn Ảnh Từ Thư Viện / Máy Ảnh'),
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),

                    // Chọn cuộc thi
                    DropdownButtonFormField<String>(
                      value: selectedContest,
                      decoration: const InputDecoration(
                        labelText: 'Chọn cuộc thi tham gia',
                        border: OutlineInputBorder(),
                      ),
                      items: [
                        'Nét Đẹp Đô Thị Việt Nam 2026',
                        'Khoảnh Khắc Đen Trắng & Hoài Niệm',
                        'Hơi Thở Thiên Nhiên & Con Người',
                      ]
                          .map((c) => DropdownMenuItem(value: c, child: Text(c, overflow: TextOverflow.ellipsis)))
                          .toList(),
                      onChanged: (val) => setModalState(() => selectedContest = val!),
                    ),
                    const SizedBox(height: 12),

                    TextField(
                      controller: titleCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Tên tác phẩm / Tiêu đề khung hình',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: stockCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Loại Film (Film Stock)',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),

                    Row(
                      children: [
                        Expanded(
                          child: DropdownButtonFormField<int>(
                            value: selectedIso,
                            decoration: const InputDecoration(
                              labelText: 'ISO',
                              border: OutlineInputBorder(),
                            ),
                            items: [100, 200, 400, 800, 1600]
                                .map((iso) => DropdownMenuItem(value: iso, child: Text('ISO $iso')))
                                .toList(),
                            onChanged: (val) => setModalState(() => selectedIso = val!),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: TextField(
                            controller: shutterCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Tốc độ màn trập',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),

                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: apertureCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Khẩu độ',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: TextField(
                            controller: locationCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Địa điểm chụp',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),

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
                            if (editItem == null) {
                              _submissions.insert(
                                0,
                                ContestSubmission(
                                  id: 'SUB-0${_submissions.length + 1}',
                                  contestTitle: selectedContest,
                                  imagePath: imagePreview,
                                  title: titleCtrl.text.trim().isEmpty ? 'Khung hình mới' : titleCtrl.text.trim(),
                                  filmStock: stockCtrl.text.trim(),
                                  iso: selectedIso,
                                  shutterSpeed: shutterCtrl.text.trim(),
                                  aperture: apertureCtrl.text.trim(),
                                  location: locationCtrl.text.trim(),
                                  status: 'Đang chấm',
                                  submittedAt: DateTime.now(),
                                ),
                              );
                            } else {
                              final index = _submissions.indexOf(editItem);
                              _submissions[index] = editItem.copyWith(
                                contestTitle: selectedContest,
                                imagePath: imagePreview,
                                title: titleCtrl.text.trim(),
                                filmStock: stockCtrl.text.trim(),
                                iso: selectedIso,
                                shutterSpeed: shutterCtrl.text.trim(),
                                aperture: apertureCtrl.text.trim(),
                                location: locationCtrl.text.trim(),
                              );
                            }
                          });
                          Navigator.pop(ctx);
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Đã lưu và cập nhật bài dự thi thành công!')),
                          );
                        },
                        child: Text(editItem == null ? 'Nộp Bài Dự Thi' : 'Cập Nhật Bài Nộp'),
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
      backgroundColor: const Color(0xFFF6F5F2),
      appBar: AppBar(
        title: const Text('Quản Lý Bài Dự Thi & Metadata (FE7)'),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _submissions.length,
        itemBuilder: (context, index) {
          final sub = _submissions[index];
          final isApproved = sub.status == 'Đã duyệt';

          return Card(
            margin: const EdgeInsets.only(bottom: 14),
            elevation: 2,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(sub.id, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.grey)),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: isApproved ? Colors.green.shade50 : Colors.orange.shade50,
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: isApproved ? Colors.green.shade300 : Colors.orange.shade300),
                        ),
                        child: Text(
                          sub.status,
                          style: TextStyle(
                            color: isApproved ? Colors.green.shade700 : Colors.orange.shade800,
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
                        child: Image.network(sub.imagePath, width: 85, height: 75, fit: BoxFit.cover),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(sub.title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                            const SizedBox(height: 2),
                            Text('Cuộc thi: ${sub.contestTitle}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700), maxLines: 1, overflow: TextOverflow.ellipsis),
                            Text('Film: ${sub.filmStock} (ISO ${sub.iso}) • ${sub.shutterSpeed} • ${sub.aperture}', style: TextStyle(fontSize: 11, color: Colors.grey.shade600)),
                            const SizedBox(height: 6),
                            Row(
                              children: [
                                Icon(Icons.location_on, size: 13, color: Colors.amber.shade800),
                                const SizedBox(width: 4),
                                Text(sub.location, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                                const Spacer(),
                                TextButton.icon(
                                  style: TextButton.styleFrom(foregroundColor: Colors.amber.shade900, padding: EdgeInsets.zero),
                                  onPressed: () => _showAddOrEditDialog(editItem: sub),
                                  icon: const Icon(Icons.edit, size: 14),
                                  label: const Text('Sửa', style: TextStyle(fontSize: 12)),
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
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: Colors.amber.shade800,
        foregroundColor: Colors.white,
        onPressed: () => _showAddOrEditDialog(),
        icon: const Icon(Icons.add_a_photo),
        label: const Text('Nộp Ảnh & Metadata'),
      ),
    );
  }
}
