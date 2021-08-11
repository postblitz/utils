import random


class Sort:
    def __init__(self, nums):
        self.nums = nums
        self.n = len(nums)
        self.max_n = max(nums)
        print('n=%s max=%s' % (self.n, self.max_n))

    def count(self):
        V = [0] * (self.max_n + 1)
        for i in range(0, self.n):
            V[self.nums[i]] += 1
        k = 0
        for i in range(self.max_n + 1):
            for j in range(0, V[i]):
                self.nums[k] = i
                k += 1
        del V

    def bubble(self):
        is_sorted = False
        for i in range(self.n):
            if is_sorted is True:
                break
            is_sorted = True
            for j in range(self.n - i - 1):
                if self.nums[j] > self.nums[j + 1]:
                    is_sorted = False
                    self.nums[j], self.nums[j + 1] = self.nums[j + 1], self.nums[j]

    def insert(self):
        for i in range(1, self.n):
            v = self.nums[i]
            j = i - 1
            while j >= 0 and self.nums[j] > v:
                self.nums[j + 1] = self.nums[j]
                j -= 1
            self.nums[j + 1] = v

    def quick_slow(self, left, right):
        if left < right:
            p = self._part(left, right)
            self.quick_slow(left, p)
            self.quick_slow(p + 1, right)

    def quick_fast(self, left, right):
        while left < right:
            p = self._part_rand(left, right)
            if p - left < right - p - 1:
                self.quick_fast(left, p)
                left = p + 1
            else:
                self.quick_fast(p + 1, right)
                right = p

    def _part_rand(self, left, right):
        poz = random.randint(left, right)
        self.nums[poz], self.nums[left] = self.nums[left], self.nums[poz]
        return self._part(left, right)

    def _part(self, left, right):
        v = self.nums[left]
        left -= 1
        right += 1
        while left < right:
            right -= 1
            while left < right and self.nums[right] > v:
                right -= 1
            left += 1
            while left < right and self.nums[left] < v:
                left += 1
            if left < right:
                self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
        return right

    def merge(self, left, right):
        if left < right:
            m = (left + right) // 2
            self.merge(left, m)
            self.merge(m + 1, right)
            self._mix1(left, m, right)

    def _mix1(self, left, m, right):
        b = []
        i = left
        j = m + 1
        print('mix(%s,%s)' % (self.nums[left:m + 1], self.nums[m + 1:right + 1]))
        while i <= m and j <= right:
            if self.nums[i] <= self.nums[j]:
                b.append(self.nums[i])
                i += 1
            else:
                b.append(self.nums[j])
                j += 1
        while i <= m:
            b.append(self.nums[i])
            i += 1
        while j <= right:
            b.append(self.nums[j])
            j += 1
        for i in range(len(b)):
            self.nums[left + i] = b[i]
        del b


if __name__ == '__main__':
    x = Sort(nums=[5,3,9,2,1,8,4,7])
    x.merge(0,5)
    print(x.nums)
