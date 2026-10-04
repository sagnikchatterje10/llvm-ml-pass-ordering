"""
Benchmark Generator for LLVM ML Pass Project.
Generates 40 distinct, realistic C benchmark programs covering diverse computational patterns:
- loops and nested loops
- arrays and memory operations
- arithmetic and bitwise math
- conditional branches and switch dispatch
- function calls and recursion
- pointers and structs
- algorithms (sorting, searching, DP, numerical)
"""

import os
import json
from pathlib import Path

BENCHMARKS = [
    # 1. arrays_loops
    {
        "id": "PG001",
        "name": "vec_dot",
        "category": "arrays_loops",
        "split": "train",
        "description": "Vector dot product with accumulation and stride",
        "code": """#include <stdio.h>

long long vec_dot(const int *a, const int *b, int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += (long long)a[i] * b[i];
    }
    return sum;
}

int main(void) {
    int a[16] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    int b[16] = {16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    long long res = vec_dot(a, b, 16);
    return (int)(res & 0xFF);
}
"""
    },
    {
        "id": "PG002",
        "name": "matrix_mult",
        "category": "arrays_loops",
        "split": "train",
        "description": "2D Square Matrix multiplication with nested triple loops",
        "code": """#include <stdio.h>

#define N 8

void matmul(const int a[N][N], const int b[N][N], int c[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int acc = 0;
            for (int k = 0; k < N; k++) {
                acc += a[i][k] * b[k][j];
            }
            c[i][j] = acc;
        }
    }
}

int main(void) {
    int a[N][N], b[N][N], c[N][N];
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            a[i][j] = (i + j) & 7;
            b[i][j] = (i * j + 1) & 7;
            c[i][j] = 0;
        }
    }
    matmul(a, b, c);
    return c[0][0] + c[N-1][N-1];
}
"""
    },
    {
        "id": "PG003",
        "name": "prefix_sum",
        "category": "arrays_loops",
        "split": "train",
        "description": "Array prefix sum (scan) with in-place bounds checking",
        "code": """#include <stdio.h>

void prefix_sum(int *arr, int *out, int n) {
    if (n <= 0) return;
    out[0] = arr[0];
    for (int i = 1; i < n; i++) {
        out[i] = out[i - 1] + arr[i];
    }
}

int main(void) {
    int data[20];
    int result[20];
    for (int i = 0; i < 20; i++) data[i] = i * 2 + 1;
    prefix_sum(data, result, 20);
    return result[19] & 0x7F;
}
"""
    },
    {
        "id": "PG004",
        "name": "array_rotate",
        "category": "arrays_loops",
        "split": "train",
        "description": "Array block reversal and cyclic rotation",
        "code": """#include <stdio.h>

static void reverse_range(int *arr, int start, int end) {
    while (start < end) {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}

void rotate_left(int *arr, int n, int k) {
    if (n <= 0) return;
    k = k % n;
    if (k < 0) k += n;
    reverse_range(arr, 0, k - 1);
    reverse_range(arr, k, n - 1);
    reverse_range(arr, 0, n - 1);
}

int main(void) {
    int arr[12] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
    rotate_left(arr, 12, 5);
    return arr[0] + arr[11];
}
"""
    },
    {
        "id": "PG005",
        "name": "conv2d",
        "category": "arrays_loops",
        "split": "test",  # Test set
        "description": "2D Image convolution kernel filtering with edge clamping",
        "code": """#include <stdio.h>

#define W 10
#define H 10

void conv2d(const int in[H][W], int out[H][W], const int kernel[3][3]) {
    for (int y = 1; y < H - 1; y++) {
        for (int x = 1; x < W - 1; x++) {
            int acc = 0;
            for (int ky = -1; ky <= 1; ky++) {
                for (int kx = -1; kx <= 1; kx++) {
                    acc += in[y + ky][x + kx] * kernel[ky + 1][kx + 1];
                }
            }
            out[y][x] = acc / 9;
        }
    }
}

int main(void) {
    int in[H][W], out[H][W] = {0};
    int k[3][3] = {{1, 1, 1}, {1, 2, 1}, {1, 1, 1}};
    for (int i = 0; i < H; i++)
        for (int j = 0; j < W; j++)
            in[i][j] = (i * 3 + j) % 256;
    conv2d(in, out, k);
    return out[5][5] & 0xFF;
}
"""
    },

    # 2. sorting_searching
    {
        "id": "PG006",
        "name": "bubble_sort",
        "category": "sorting_searching",
        "split": "train",
        "description": "Bubble sort with early exit flag and element swap",
        "code": """#include <stdio.h>

void bubble_sort(int *arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
                swapped = 1;
            }
        }
        if (!swapped) break;
    }
}

int main(void) {
    int nums[10] = {64, 34, 25, 12, 22, 11, 90, 88, 76, 45};
    bubble_sort(nums, 10);
    return nums[0] + nums[9];
}
"""
    },
    {
        "id": "PG007",
        "name": "insertion_sort",
        "category": "sorting_searching",
        "split": "train",
        "description": "Insertion sort algorithm shifting elements",
        "code": """#include <stdio.h>

void insertion_sort(int *arr, int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

int main(void) {
    int nums[10] = {12, 11, 13, 5, 6, 7, 2, 45, 9, 1};
    insertion_sort(nums, 10);
    return nums[0] + nums[5];
}
"""
    },
    {
        "id": "PG008",
        "name": "selection_sort",
        "category": "sorting_searching",
        "split": "train",
        "description": "Selection sort finding minimum index each pass",
        "code": """#include <stdio.h>

void selection_sort(int *arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            int tmp = arr[i];
            arr[i] = arr[min_idx];
            arr[min_idx] = tmp;
        }
    }
}

int main(void) {
    int a[8] = {29, 10, 14, 37, 13, 5, 2, 99};
    selection_sort(a, 8);
    return a[0] + a[7];
}
"""
    },
    {
        "id": "PG009",
        "name": "binary_search",
        "category": "sorting_searching",
        "split": "train",
        "description": "Iterative binary search with conditional midpoint updates",
        "code": """#include <stdio.h>

int binary_search(const int *arr, int n, int target) {
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main(void) {
    int sorted[16] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 100, 120, 135, 140, 150, 160};
    int r1 = binary_search(sorted, 16, 23);
    int r2 = binary_search(sorted, 16, 999);
    return r1 + (r2 == -1 ? 1 : 0);
}
"""
    },
    {
        "id": "PG010",
        "name": "quicksort",
        "category": "sorting_searching",
        "split": "test",  # Test set
        "description": "Recursive QuickSort with Lomuto partition scheme",
        "code": """#include <stdio.h>

static void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

static int partition(int *arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quicksort(int *arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

int main(void) {
    int arr[10] = {10, 80, 30, 90, 40, 50, 70, 20, 60, 5};
    quicksort(arr, 0, 9);
    return arr[0] + arr[9];
}
"""
    },

    # 3. recursion
    {
        "id": "PG011",
        "name": "fib_recursive",
        "category": "recursion",
        "split": "train",
        "description": "Recursive Fibonacci with base conditions",
        "code": """#include <stdio.h>

int fib(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    int val = fib(10);
    return val & 0xFF;
}
"""
    },
    {
        "id": "PG012",
        "name": "factorial",
        "category": "recursion",
        "split": "train",
        "description": "Recursive factorial calculation",
        "code": """#include <stdio.h>

long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main(void) {
    long long f = factorial(8);
    return (int)(f % 256);
}
"""
    },
    {
        "id": "PG013",
        "name": "hanoi",
        "category": "recursion",
        "split": "train",
        "description": "Towers of Hanoi move counter recursion",
        "code": """#include <stdio.h>

int hanoi_moves(int n, char from, char to, char aux) {
    if (n == 1) return 1;
    int moves = hanoi_moves(n - 1, from, aux, to);
    moves += 1;
    moves += hanoi_moves(n - 1, aux, to, from);
    return moves;
}

int main(void) {
    int total = hanoi_moves(5, 'A', 'C', 'B');
    return total & 0x7F;
}
"""
    },
    {
        "id": "PG014",
        "name": "ackermann",
        "category": "recursion",
        "split": "train",
        "description": "Ackermann-Peter recursive function",
        "code": """#include <stdio.h>

int ackermann(int m, int n) {
    if (m == 0) return n + 1;
    if (m > 0 && n == 0) return ackermann(m - 1, 1);
    return ackermann(m - 1, ackermann(m, n - 1));
}

int main(void) {
    int res = ackermann(2, 3);
    return res & 0xFF;
}
"""
    },
    {
        "id": "PG015",
        "name": "tree_traverse",
        "category": "recursion",
        "split": "test",  # Test set
        "description": "Recursive binary tree depth-first sum and height",
        "code": """#include <stdio.h>

struct TreeNode {
    int val;
    int left_idx;
    int right_idx;
};

int tree_sum(const struct TreeNode *nodes, int idx) {
    if (idx < 0) return 0;
    int s = nodes[idx].val;
    s += tree_sum(nodes, nodes[idx].left_idx);
    s += tree_sum(nodes, nodes[idx].right_idx);
    return s;
}

int main(void) {
    struct TreeNode nodes[5] = {
        {10, 1, 2},
        {5, 3, 4},
        {15, -1, -1},
        {2, -1, -1},
        {7, -1, -1}
    };
    int total = tree_sum(nodes, 0);
    return total & 0xFF;
}
"""
    },

    # 4. arithmetic_math
    {
        "id": "PG016",
        "name": "fast_power",
        "category": "arithmetic_math",
        "split": "train",
        "description": "Binary modular exponentiation (fast power)",
        "code": """#include <stdio.h>

long long mod_pow(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}

int main(void) {
    long long r = mod_pow(7, 25, 1000000007);
    return (int)(r & 0xFF);
}
"""
    },
    {
        "id": "PG017",
        "name": "gcd_lcm",
        "category": "arithmetic_math",
        "split": "train",
        "description": "Euclidean GCD and LCM calculation",
        "code": """#include <stdio.h>

int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}

long long lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    return ((long long)a / gcd(a, b)) * b;
}

int main(void) {
    int g = gcd(48, 180);
    long long l = lcm(48, 180);
    return (int)((g + l) & 0xFF);
}
"""
    },
    {
        "id": "PG018",
        "name": "sieve",
        "category": "arithmetic_math",
        "split": "train",
        "description": "Sieve of Eratosthenes prime counter",
        "code": """#include <stdio.h>

int count_primes(int limit) {
    char is_prime[100];
    for (int i = 0; i < limit; i++) is_prime[i] = 1;
    is_prime[0] = is_prime[1] = 0;
    for (int p = 2; p * p < limit; p++) {
        if (is_prime[p]) {
            for (int i = p * p; i < limit; i += p) {
                is_prime[i] = 0;
            }
        }
    }
    int count = 0;
    for (int i = 2; i < limit; i++) {
        if (is_prime[i]) count++;
    }
    return count;
}

int main(void) {
    return count_primes(100);
}
"""
    },
    {
        "id": "PG019",
        "name": "sqrt_newton",
        "category": "arithmetic_math",
        "split": "train",
        "description": "Floating-point Newton-Raphson square root method",
        "code": """#include <stdio.h>

double sqrt_newton(double n) {
    if (n < 0) return -1.0;
    if (n == 0) return 0.0;
    double x = n;
    for (int i = 0; i < 20; i++) {
        double root = 0.5 * (x + (n / x));
        double diff = root - x;
        if (diff < 0) diff = -diff;
        if (diff < 1e-6) return root;
        x = root;
    }
    return x;
}

int main(void) {
    double s = sqrt_newton(256.0);
    return (int)s;
}
"""
    },
    {
        "id": "PG020",
        "name": "horner_eval",
        "category": "arithmetic_math",
        "split": "test",  # Test set
        "description": "Polynomial evaluation using Horner's rule",
        "code": """#include <stdio.h>

double horner(const double *coeffs, int degree, double x) {
    double res = coeffs[0];
    for (int i = 1; i <= degree; i++) {
        res = res * x + coeffs[i];
    }
    return res;
}

int main(void) {
    double poly[5] = {3.0, -2.0, 5.0, -1.0, 7.0};
    double r = horner(poly, 4, 2.5);
    return (int)r & 0xFF;
}
"""
    },

    # 5. bitwise_logic
    {
        "id": "PG021",
        "name": "popcount",
        "category": "bitwise_logic",
        "split": "train",
        "description": "Branchless parallel bit counting / population count",
        "code": """#include <stdio.h>

unsigned int popcount(unsigned int v) {
    v = v - ((v >> 1) & 0x55555555);
    v = (v & 0x33333333) + ((v >> 2) & 0x33333333);
    return (((v + (v >> 4)) & 0xF0F0F0F) * 0x1010101) >> 24;
}

int main(void) {
    unsigned int test_vals[8] = {0, 1, 0xFF, 0x12345678, 0xAAAAAAAA, 0x55555555, 0xFFFFFFFF, 42};
    unsigned int acc = 0;
    for (int i = 0; i < 8; i++) acc += popcount(test_vals[i]);
    return (int)(acc & 0xFF);
}
"""
    },
    {
        "id": "PG022",
        "name": "crc32",
        "category": "bitwise_logic",
        "split": "train",
        "description": "Bitwise CRC32 calculation kernel",
        "code": """#include <stdio.h>

unsigned int crc32_simple(const unsigned char *data, int len) {
    unsigned int crc = 0xFFFFFFFF;
    for (int i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
            else
                crc >>= 1;
        }
    }
    return ~crc;
}

int main(void) {
    unsigned char msg[] = "Compiler Optimization ML 2026";
    unsigned int c = crc32_simple(msg, sizeof(msg) - 1);
    return (int)(c & 0x7F);
}
"""
    },
    {
        "id": "PG023",
        "name": "bit_reverse",
        "category": "bitwise_logic",
        "split": "train",
        "description": "Reversal of bits in 32-bit unsigned integer",
        "code": """#include <stdio.h>

unsigned int reverse_bits(unsigned int n) {
    n = ((n >> 1) & 0x55555555) | ((n & 0x55555555) << 1);
    n = ((n >> 2) & 0x33333333) | ((n & 0x33333333) << 2);
    n = ((n >> 4) & 0x0F0F0F0F) | ((n & 0x0F0F0F0F) << 4);
    n = ((n >> 8) & 0x00FF00FF) | ((n & 0x00FF00FF) << 8);
    return (n >> 16) | (n << 16);
}

int main(void) {
    unsigned int r = reverse_bits(0x12345678);
    return (int)(r & 0xFF);
}
"""
    },
    {
        "id": "PG024",
        "name": "lfsr_prng",
        "category": "bitwise_logic",
        "split": "train",
        "description": "Linear Feedback Shift Register pseudo-random sequence",
        "code": """#include <stdio.h>

unsigned int lfsr_step(unsigned int *lfsr) {
    unsigned int bit = ((*lfsr >> 0) ^ (*lfsr >> 2) ^ (*lfsr >> 3) ^ (*lfsr >> 5)) & 1;
    *lfsr = (*lfsr >> 1) | (bit << 15);
    return *lfsr;
}

int main(void) {
    unsigned int state = 0xACE1;
    unsigned int sum = 0;
    for (int i = 0; i < 50; i++) {
        sum += lfsr_step(&state);
    }
    return (int)(sum & 0xFF);
}
"""
    },

    # 6. strings_pointers
    {
        "id": "PG025",
        "name": "string_ops",
        "category": "strings_pointers",
        "split": "train",
        "description": "Pointer-based string copy, length, and reverse",
        "code": """#include <stdio.h>

int str_len(const char *s) {
    const char *p = s;
    while (*p) p++;
    return (int)(p - s);
}

void str_cpy(char *dest, const char *src) {
    while ((*dest++ = *src++));
}

int main(void) {
    const char *msg = "Optimizing LLVM IR";
    char buf[32];
    str_cpy(buf, msg);
    return str_len(buf);
}
"""
    },
    {
        "id": "PG026",
        "name": "str_search",
        "category": "strings_pointers",
        "split": "test",  # Test set
        "description": "Pointer-based naive substring search with offset returns",
        "code": """#include <stdio.h>

int str_find(const char *haystack, const char *needle) {
    if (!*needle) return 0;
    for (int i = 0; haystack[i] != '\\0'; i++) {
        int match = 1;
        for (int j = 0; needle[j] != '\\0'; j++) {
            if (haystack[i + j] == '\\0' || haystack[i + j] != needle[j]) {
                match = 0;
                break;
            }
        }
        if (match) return i;
    }
    return -1;
}

int main(void) {
    const char *h = "the quick brown fox jumps over the lazy dog";
    const char *n = "fox";
    return str_find(h, n);
}
"""
    },
    {
        "id": "PG027",
        "name": "palindrome",
        "category": "strings_pointers",
        "split": "train",
        "description": "Two-pointer bidirectional palindrome validator",
        "code": """#include <stdio.h>

int is_palindrome(const char *s, int len) {
    const char *left = s;
    const char *right = s + len - 1;
    while (left < right) {
        if (*left != *right) return 0;
        left++;
        right--;
    }
    return 1;
}

int main(void) {
    const char w1[] = "racecar";
    const char w2[] = "compiler";
    int r1 = is_palindrome(w1, 7);
    int r2 = is_palindrome(w2, 8);
    return r1 + (r2 ? 0 : 2);
}
"""
    },
    {
        "id": "PG028",
        "name": "run_length",
        "category": "strings_pointers",
        "split": "train",
        "description": "Run-length byte sequence encoder",
        "code": """#include <stdio.h>

int rle_encode(const char *src, int n, char *out) {
    if (n <= 0) return 0;
    int out_idx = 0;
    int i = 0;
    while (i < n) {
        int run = 1;
        while (i + 1 < n && src[i] == src[i + 1] && run < 255) {
            run++;
            i++;
        }
        out[out_idx++] = (char)run;
        out[out_idx++] = src[i];
        i++;
    }
    return out_idx;
}

int main(void) {
    const char raw[] = "AAABBBCCCCDD";
    char compressed[32];
    int len = rle_encode(raw, 12, compressed);
    return len;
}
"""
    },

    # 7. memory_structs
    {
        "id": "PG029",
        "name": "linked_list",
        "category": "memory_structs",
        "split": "val",  # Val set
        "description": "Singly linked list node traversal and node filtering",
        "code": """#include <stdio.h>

struct Node {
    int data;
    int next_idx;
};

int filter_sum(const struct Node *pool, int head, int threshold) {
    int sum = 0;
    int curr = head;
    while (curr >= 0) {
        if (pool[curr].data > threshold) {
            sum += pool[curr].data;
        }
        curr = pool[curr].next_idx;
    }
    return sum;
}

int main(void) {
    struct Node pool[6] = {
        {10, 1}, {25, 2}, {5, 3}, {40, 4}, {15, 5}, {30, -1}
    };
    int s = filter_sum(pool, 0, 15);
    return s & 0xFF;
}
"""
    },
    {
        "id": "PG030",
        "name": "ring_buffer",
        "category": "memory_structs",
        "split": "val",  # Val set
        "description": "Circular ring buffer push, pop, and status calculation",
        "code": """#include <stdio.h>

#define CAP 8

struct RingBuffer {
    int buffer[CAP];
    int head;
    int tail;
    int count;
};

void rb_init(struct RingBuffer *rb) {
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

int rb_push(struct RingBuffer *rb, int val) {
    if (rb->count == CAP) return 0;
    rb->buffer[rb->tail] = val;
    rb->tail = (rb->tail + 1) % CAP;
    rb->count++;
    return 1;
}

int rb_pop(struct RingBuffer *rb, int *val) {
    if (rb->count == 0) return 0;
    *val = rb->buffer[rb->head];
    rb->head = (rb->head + 1) % CAP;
    rb->count--;
    return 1;
}

int main(void) {
    struct RingBuffer rb;
    rb_init(&rb);
    for (int i = 0; i < 6; i++) rb_push(&rb, i * 10);
    int v1, v2;
    rb_pop(&rb, &v1);
    rb_pop(&rb, &v2);
    return (v1 + v2 + rb.count) & 0xFF;
}
"""
    },
    {
        "id": "PG031",
        "name": "min_heap",
        "category": "memory_structs",
        "split": "val",  # Val set
        "description": "Min-heap priority queue sift up/down operations",
        "code": """#include <stdio.h>

static void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

void heapify(int *arr, int n, int i) {
    int smallest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] < arr[smallest]) smallest = left;
    if (right < n && arr[right] < arr[smallest]) smallest = right;

    if (smallest != i) {
        swap(&arr[i], &arr[smallest]);
        heapify(arr, n, smallest);
    }
}

void build_min_heap(int *arr, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
}

int main(void) {
    int heap[9] = {12, 11, 13, 5, 6, 7, 3, 20, 1};
    build_min_heap(heap, 9);
    return heap[0] + heap[1];
}
"""
    },
    {
        "id": "PG032",
        "name": "struct_stats",
        "category": "memory_structs",
        "split": "val",  # Val set
        "description": "Statistical summary across array of structures",
        "code": """#include <stdio.h>

struct Item {
    int id;
    int weight;
    int value;
};

void compute_stats(const struct Item *items, int n, int *total_weight, int *max_value) {
    *total_weight = 0;
    *max_value = -1;
    for (int i = 0; i < n; i++) {
        *total_weight += items[i].weight;
        if (items[i].value > *max_value) {
            *max_value = items[i].value;
        }
    }
}

int main(void) {
    struct Item list[5] = {
        {1, 10, 60},
        {2, 20, 100},
        {3, 30, 120},
        {4, 15, 75},
        {5, 25, 95}
    };
    int tw, mv;
    compute_stats(list, 5, &tw, &mv);
    return (tw + mv) & 0xFF;
}
"""
    },

    # 8. control_flow_switch
    {
        "id": "PG033",
        "name": "state_machine",
        "category": "control_flow_switch",
        "split": "val",  # Val set
        "description": "Finite State Machine with transition table and switch dispatch",
        "code": """#include <stdio.h>

typedef enum { STATE_IDLE, STATE_ACTIVE, STATE_WAITING, STATE_DONE, STATE_ERROR } State;

State step_fsm(State s, int event) {
    switch (s) {
        case STATE_IDLE:
            return (event == 1) ? STATE_ACTIVE : STATE_IDLE;
        case STATE_ACTIVE:
            if (event == 0) return STATE_WAITING;
            if (event == 2) return STATE_DONE;
            if (event == 9) return STATE_ERROR;
            return STATE_ACTIVE;
        case STATE_WAITING:
            return (event == 1) ? STATE_ACTIVE : STATE_DONE;
        case STATE_DONE:
        case STATE_ERROR:
        default:
            return STATE_IDLE;
    }
}

int main(void) {
    State s = STATE_IDLE;
    int events[6] = {1, 0, 1, 2, 0, 1};
    for (int i = 0; i < 6; i++) {
        s = step_fsm(s, events[i]);
    }
    return (int)s;
}
"""
    },
    {
        "id": "PG034",
        "name": "opcode_interpreter",
        "category": "control_flow_switch",
        "split": "val",  # Val set
        "description": "Bytecode VM opcode loop with jump switch statement",
        "code": """#include <stdio.h>

#define OP_NOP 0
#define OP_ADD 1
#define OP_SUB 2
#define OP_MUL 3
#define OP_HALT 4

int run_vm(const int *ops, int len) {
    int acc = 0;
    for (int pc = 0; pc < len; pc += 2) {
        int opcode = ops[pc];
        int operand = ops[pc + 1];
        switch (opcode) {
            case OP_NOP:
                break;
            case OP_ADD:
                acc += operand;
                break;
            case OP_SUB:
                acc -= operand;
                break;
            case OP_MUL:
                acc *= operand;
                break;
            case OP_HALT:
                return acc;
            default:
                acc = -1;
                return acc;
        }
    }
    return acc;
}

int main(void) {
    int program[10] = {OP_ADD, 15, OP_MUL, 3, OP_SUB, 5, OP_HALT, 0, OP_ADD, 99};
    int res = run_vm(program, 10);
    return res & 0xFF;
}
"""
    },
    {
        "id": "PG035",
        "name": "decision_tree",
        "category": "control_flow_switch",
        "split": "test",  # Test set
        "description": "Deep nested conditional classification tree",
        "code": """#include <stdio.h>

int classify_point(int x, int y, int z) {
    if (x > 10) {
        if (y < 20) {
            if (z >= 5) return 1;
            else return 2;
        } else {
            if (z % 2 == 0) return 3;
            else return 4;
        }
    } else {
        if (y >= 50) {
            if (z < 0) return 5;
            else return 6;
        } else {
            if (x == y) return 7;
            else return 8;
        }
    }
}

int main(void) {
    int c1 = classify_point(15, 10, 8);
    int c2 = classify_point(5, 50, -3);
    int c3 = classify_point(2, 2, 10);
    return c1 + c2 + c3;
}
"""
    },
    {
        "id": "PG036",
        "name": "collatz",
        "category": "control_flow_switch",
        "split": "train",
        "description": "Collatz sequence loop step counter with odd/even branching",
        "code": """#include <stdio.h>

int collatz_length(long long n) {
    int steps = 0;
    while (n > 1) {
        if (n & 1) {
            n = 3 * n + 1;
        } else {
            n = n / 2;
        }
        steps++;
    }
    return steps;
}

int main(void) {
    int s1 = collatz_length(27);
    int s2 = collatz_length(19);
    return (s1 + s2) & 0xFF;
}
"""
    },

    # 9. mixed_computation
    {
        "id": "PG037",
        "name": "cellular_automata",
        "category": "mixed_computation",
        "split": "train",
        "description": "1D Wolfram Rule 30 cellular automaton evolution",
        "code": """#include <stdio.h>

#define CELLS 32

void evolve_rule30(unsigned char *state, int steps) {
    unsigned char next[CELLS];
    for (int s = 0; s < steps; s++) {
        for (int i = 0; i < CELLS; i++) {
            unsigned char left = (i > 0) ? state[i - 1] : state[CELLS - 1];
            unsigned char center = state[i];
            unsigned char right = (i < CELLS - 1) ? state[i + 1] : state[0];
            int pat = (left << 2) | (center << 1) | right;
            next[i] = (30 >> pat) & 1;
        }
        for (int i = 0; i < CELLS; i++) state[i] = next[i];
    }
}

int main(void) {
    unsigned char state[CELLS] = {0};
    state[CELLS / 2] = 1;
    evolve_rule30(state, 10);
    int count = 0;
    for (int i = 0; i < CELLS; i++) count += state[i];
    return count;
}
"""
    },
    {
        "id": "PG038",
        "name": "runge_kutta",
        "category": "mixed_computation",
        "split": "train",
        "description": "Runge-Kutta 2nd order numerical ODE integrator",
        "code": """#include <stdio.h>

static double f(double t, double y) {
    return t * y - 0.5 * y * y;
}

double rk2_integrate(double t0, double y0, double h, int steps) {
    double t = t0;
    double y = y0;
    for (int i = 0; i < steps; i++) {
        double k1 = h * f(t, y);
        double k2 = h * f(t + h, y + k1);
        y += 0.5 * (k1 + k2);
        t += h;
    }
    return y;
}

int main(void) {
    double res = rk2_integrate(0.0, 1.0, 0.05, 20);
    return (int)(res * 10.0) & 0xFF;
}
"""
    },
    {
        "id": "PG039",
        "name": "hash_table",
        "category": "mixed_computation",
        "split": "train",
        "description": "Open-addressing linear probing integer hash map",
        "code": """#include <stdio.h>

#define TABLE_SIZE 16

struct HashEntry {
    int key;
    int value;
    int occupied;
};

void ht_init(struct HashEntry *table) {
    for (int i = 0; i < TABLE_SIZE; i++) table[i].occupied = 0;
}

void ht_insert(struct HashEntry *table, int key, int val) {
    int idx = (key >= 0 ? key : -key) % TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        if (!table[pos].occupied || table[pos].key == key) {
            table[pos].key = key;
            table[pos].value = val;
            table[pos].occupied = 1;
            return;
        }
    }
}

int ht_lookup(const struct HashEntry *table, int key) {
    int idx = (key >= 0 ? key : -key) % TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        if (!table[pos].occupied) return -1;
        if (table[pos].key == key) return table[pos].value;
    }
    return -1;
}

int main(void) {
    struct HashEntry ht[TABLE_SIZE];
    ht_init(ht);
    ht_insert(ht, 101, 500);
    ht_insert(ht, 117, 600); // hash collision (101%16 == 117%16 == 5)
    ht_insert(ht, 202, 700);
    int v1 = ht_lookup(ht, 101);
    int v2 = ht_lookup(ht, 117);
    return (v1 + v2) & 0xFF;
}
"""
    },
    {
        "id": "PG040",
        "name": "knapsack",
        "category": "mixed_computation",
        "split": "test",  # Test set
        "description": "0-1 Knapsack dynamic programming table solver",
        "code": """#include <stdio.h>

#define MAX(a, b) ((a) > (b) ? (a) : (b))

int knapsack(int W, const int *wt, const int *val, int n) {
    int dp[16][32] = {0};
    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= W; w++) {
            if (wt[i - 1] <= w) {
                dp[i][w] = MAX(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    return dp[n][W];
}

int main(void) {
    int val[4] = {60, 100, 120, 80};
    int wt[4] = {10, 20, 30, 15};
    int W = 30;
    int res = knapsack(W, wt, val, 4);
    return res & 0xFF;
}
"""
    }
]

def generate_benchmarks():
    base_dir = Path("benchmarks")
    train_dir = base_dir / "train"
    test_dir = base_dir / "test"
    val_dir = base_dir / "val"
    meta_dir = base_dir / "metadata"

    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    manifest = []

    for b in BENCHMARKS:
        filename = f"{b['id']}_{b['name']}.c"
        if b["split"] == "train":
            target_path = train_dir / filename
        elif b["split"] == "test":
            target_path = test_dir / filename
        else: # val
            target_path = val_dir / filename

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(b["code"].strip() + "\n")

        manifest_entry = {
            "program_id": b["id"],
            "name": b["name"],
            "category": b["category"],
            "split": b["split"],
            "source_file": str(target_path.as_posix()),
            "description": b["description"]
        }
        manifest.append(manifest_entry)

    manifest_file = meta_dir / "manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(BENCHMARKS)} benchmark programs.")
    split_counts = {}
    for b in BENCHMARKS:
        split_counts[b["split"]] = split_counts.get(b["split"], 0) + 1
    for s, cnt in split_counts.items():
        print(f"  Split '{s}': {cnt} programs ({cnt/len(BENCHMARKS)*100:.1f}%)")
    print(f"Manifest saved to: {manifest_file}")

if __name__ == "__main__":
    generate_benchmarks()
