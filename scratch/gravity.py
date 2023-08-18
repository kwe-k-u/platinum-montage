from collections import Counter

# Your data array
data = [85, 88, 91, 94, 97, 103, 106, 109, 112, 115, 118, 136, 142, 148, 157, 163, 187, 196, 199, 202, 205, 220, 229, 232, 235, 238, 241, 244, 247, 250,
253, 256, 259, 262, 265, 268, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 307, 310, 313, 316, 328, 331, 334, 337, 340, 343, 346, 349, 352, 355, 358, 361, 364, 376, 379, 382, 385, 388, 391, 394, 397, 400, 403, 406, 412, 421, 424, 427, 430, 439, 445, 448, 454, 460, 466, 469, 472, 475, 478, 481, 484, 487, 490, 493, 496, 499, 85, 88, 91, 94, 97, 103, 106, 109, 112, 115, 118, 136, 142, 148, 157, 163, 187, 196, 199, 202, 205, 220, 229, 232, 235, 238, 241, 244, 247, 250, 253, 256, 259, 262, 265, 268, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 307, 310, 313, 316, 328, 331, 334, 337, 340, 343, 346, 349, 352, 355, 358, 361, 364, 376, 379, 382, 385, 388, 391, 394, 397, 400, 403, 406, 412, 421, 424,
427, 430, 439, 445, 448, 454, 460, 466, 469, 472, 475, 478, 481, 484, 487, 490, 493, 496, 499]
def find_modes(data, threshold):
    clusters = []
    current_cluster = [data[0]]

    for i in range(1, len(data)):
        if abs(data[i] - current_cluster[-1]) <= threshold:
            current_cluster.append(data[i])
        else:
            clusters.append(current_cluster)
            current_cluster = [data[i]]

    clusters.append(current_cluster)
    return clusters
# Set the window size for mode detection

distances = [data[i+1] - data[i] for i in range(len(data) - 1)]
median_distance = sorted(distances)[len(distances) // 2]
window_size = int(median_distance * 2)  # Adjust the multiplier as needed

# window_size = 10

# Find modes (potential cluster centers)
cluster_centers = find_modes(data, window_size)
print(cluster_centers)

# Print the cluster centers
for center in cluster_centers:
    print("cluster size")
    # print(f"Cluster center: {center}")
