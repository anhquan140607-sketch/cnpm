import 'package:flutter/material.dart';
import '../models/film_roll_model.dart';

class FilmRollManagerScreen extends StatefulWidget {
  const FilmRollManagerScreen({super.key});

  @override
  State<FilmRollManagerScreen> createState() => _FilmRollManagerScreenState();
}

class _FilmRollManagerScreenState extends State<FilmRollManagerScreen> {
  final FilmRoll _sampleRoll = FilmRoll(
    id: 'ROLL-01',
    rollName: 'Cuộn #01 - Sài Gòn Xưa & Nay',
    filmStock: 'Kodak Portra 400',
    iso: 400,
    totalFrames: 36,
    contestName: 'Nét Đẹp Đô Thị 2026',
    frames: List.generate(36, (index) {
      final num = index + 1;
      if (num <= 12) {
        return FilmFrame(
          frameNumber: num,
          imageUrl: 'https://picsum.photos/seed/frame_$num/600/400',
          title: 'Khung hình #$num - Phố cổ',
          location: 'Quận 1, TP.HCM',
          shutterSpeed: '1/250s',
          aperture: 'f/2.8',
          notes: 'Đo sáng tự nhiên',
          isSubmitted: num == 3 || num == 7,
        );
      }
      return FilmFrame(frameNumber: num);
    }),
  );

  void _openFrameDetail(int index) {
    final frame = _sampleRoll.frames[index];
    final titleCtrl = TextEditingController(text: frame.title ?? '');
    final locationCtrl = TextEditingController(text: frame.location ?? '');
    final shutterCtrl = TextEditingController(text: frame.shutterSpeed ?? '1/250s');
    final apertureCtrl = TextEditingController(text: frame.aperture ?? 'f/4.0');
    final notesCtrl = TextEditingController(text: frame.notes ?? '');
    bool isSubmitted = frame.isSubmitted;
    bool hasImage = frame.isExposed;

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
                          'Frame #${frame.frameNumber.toString().padLeft(2, '0')} (${_sampleRoll.filmStock})',
                          style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                        ),
                        IconButton(
                          icon: const Icon(Icons.close),
                          onPressed: () => Navigator.pop(ctx),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),

                    // Preview ảnh scan hoặc nút tải ảnh
                    Container(
                      height: 170,
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: Colors.black87,
                        borderRadius: BorderRadius.circular(12),
                        image: hasImage
                            ? DecorationImage(
                                image: NetworkImage(
                                  frame.imageUrl ?? 'https://picsum.photos/seed/new_${frame.frameNumber}/600/400',
                                ),
                                fit: BoxFit.cover,
                              )
                            : null,
                      ),
                      child: !hasImage
                          ? Center(
                              child: ElevatedButton.icon(
                                onPressed: () => setModalState(() => hasImage = true),
                                icon: const Icon(Icons.upload_file),
                                label: const Text('Tải ảnh Scan cho Frame này'),
                              ),
                            )
                          : null,
                    ),
                    const SizedBox(height: 14),

                    TextField(
                      controller: titleCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Tiêu đề khung hình / Tác phẩm',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 10),
                    TextField(
                      controller: locationCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Địa điểm chụp',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: shutterCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Tốc độ (Shutter)',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: TextField(
                            controller: apertureCtrl,
                            decoration: const InputDecoration(
                              labelText: 'Khẩu độ (Aperture)',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    TextField(
                      controller: notesCtrl,
                      maxLines: 2,
                      decoration: const InputDecoration(
                        labelText: 'Ghi chú kỹ thuật',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 10),

                    if (hasImage)
                      SwitchListTile(
                        contentPadding: EdgeInsets.zero,
                        title: const Text(
                          'Chọn khung hình này để nộp dự thi',
                          style: TextStyle(fontWeight: FontWeight.w600),
                        ),
                        subtitle: const Text('Đánh dấu gửi bài vào cuộc thi'),
                        activeColor: Colors.indigo,
                        value: isSubmitted,
                        onChanged: (val) => setModalState(() => isSubmitted = val),
                      ),
                    const SizedBox(height: 14),

                    SizedBox(
                      width: double.infinity,
                      height: 46,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF1E1E1E),
                          foregroundColor: Colors.white,
                        ),
                        onPressed: () {
                          setState(() {
                            _sampleRoll.frames[index] = frame.copyWith(
                              imageUrl: hasImage ? (frame.imageUrl ?? 'https://picsum.photos/seed/new_${frame.frameNumber}/600/400') : null,
                              title: titleCtrl.text.trim(),
                              location: locationCtrl.text.trim(),
                              shutterSpeed: shutterCtrl.text.trim(),
                              aperture: apertureCtrl.text.trim(),
                              notes: notesCtrl.text.trim(),
                              isSubmitted: hasImage ? isSubmitted : false,
                            );
                          });
                          Navigator.pop(ctx);
                        },
                        child: const Text('Lưu Thông Tin Frame'),
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
      backgroundColor: const Color(0xFF141414), // Nền bàn soi film (Light Table)
      appBar: AppBar(
        title: Text(_sampleRoll.rollName),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(14),
            color: const Color(0xFF222222),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${_sampleRoll.filmStock} • ISO ${_sampleRoll.iso}',
                      style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Đã chụp: ${_sampleRoll.exposedCount}/${_sampleRoll.totalFrames} • Đã chọn nộp: ${_sampleRoll.submittedCount}',
                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo.shade600,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: _sampleRoll.submittedCount == 0
                      ? null
                      : () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Đã gửi ${_sampleRoll.submittedCount} khung hình tới cuộc thi!'),
                            ),
                          );
                        },
                  icon: const Icon(Icons.send, size: 16),
                  label: const Text('Nộp Bài'),
                ),
              ],
            ),
          ),
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(12),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                crossAxisSpacing: 8,
                mainAxisSpacing: 10,
                childAspectRatio: 0.85,
              ),
              itemCount: _sampleRoll.frames.length,
              itemBuilder: (context, index) {
                final frame = _sampleRoll.frames[index];
                return GestureDetector(
                  onTap: () => _openFrameDetail(index),
                  child: Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFF262626),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: frame.isSubmitted
                            ? Colors.indigoAccent
                            : (frame.isExposed ? Colors.amber.shade700 : Colors.white24),
                        width: frame.isSubmitted ? 2 : 1,
                      ),
                    ),
                    child: Column(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                          color: Colors.black,
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                '#${frame.frameNumber.toString().padLeft(2, '0')}',
                                style: const TextStyle(
                                  color: Colors.amber,
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              if (frame.isSubmitted)
                                const Icon(Icons.check_circle, color: Colors.indigoAccent, size: 13),
                            ],
                          ),
                        ),
                        Expanded(
                          child: frame.isExposed
                              ? Image.network(
                                  frame.imageUrl!,
                                  width: double.infinity,
                                  fit: BoxFit.cover,
                                )
                              : const Center(
                                  child: Icon(
                                    Icons.add_a_photo_outlined,
                                    color: Colors.white38,
                                    size: 24,
                                  ),
                                ),
                        ),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(vertical: 3, horizontal: 4),
                          color: Colors.black,
                          child: Text(
                            frame.isExposed ? '${frame.shutterSpeed ?? ''} • ${frame.aperture ?? ''}' : 'Trống',
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Colors.white60, fontSize: 9),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
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
