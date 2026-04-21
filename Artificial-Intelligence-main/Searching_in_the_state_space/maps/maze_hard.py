# Tạo một bản đồ mê cung lớn hơn (ví dụ 10x10), có nhiều vật cản. Cho 2 thuật toán chạy và so sánh con số len(visited)
# Quan sát số lượng ô đã duyệt (Visited Nodes) của BFS và DFS trên bản đồ khó, từ đó rút ra kết luận thuật toán nào tối ưu bộ nhớ hơn.
maze = [
    ['S', 0,   1,   0,   0,   0,   1,   0,   0,   0],
    [1,   0,   1,   0,   1,   0,   1,   0,   1,   0],
    [0,   0,   0,   0,   1,   0,   0,   0,   1,   0],
    [0,   1,   1,   0,   1,   1,   1,   0,   1,   0],
    [0,   0,   0,   0,   0,   0,   1,   0,   1,   0],
    [1,   1,   1,   1,   1,   0,   1,   0,   1,   0],
    [0,   0,   0,   0,   1,   0,   0,   0,   1,   0],
    [0,   1,   1,   0,   1,   1,   1,   0,   1,   0],
    [0,   0,   1,   0,   0,   0,   0,   0,   1,   0],
    [1,   0,   0,   0,   1,   1,   1,   0,   0,  'G']
]